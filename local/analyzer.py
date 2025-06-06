#!/usr/bin/env python3
"""
ML Analysis Tool for Synchrophasor Data
Performs real-time and historical analysis for PDC decision making
"""
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class SynchrophasorMLAnalyzer:
    """Machine Learning analyzer for synchrophasor data"""
    
    def __init__(self, db_path='synchrophasor_data.db'):
        self.db_path = db_path
        self.models = {}
        self.init_models()
    
    def init_models(self):
        """Initialize ML models for different analysis tasks"""
        
        # Anomaly detection for frequency
        self.models['frequency_anomaly'] = IsolationForest(
            contamination=0.1,  # 10% expected anomalies
            random_state=42
        )
        
        # Anomaly detection for voltage
        self.models['voltage_anomaly'] = IsolationForest(
            contamination=0.05,  # 5% expected anomalies
            random_state=42
        )
        
        # Clustering for system states
        self.models['system_clustering'] = DBSCAN(
            eps=0.5,
            min_samples=5
        )
        
        print("🤖 ML models initialized")
    
    def load_data(self, hours_back=1):
        """Load recent data from database"""
        
        conn = sqlite3.connect(self.db_path)
        
        # Get data from last N hours
        cutoff_time = datetime.now().timestamp() - (hours_back * 3600)
        
        query = f"""
            SELECT * FROM measurements 
            WHERE timestamp > {cutoff_time}
            ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def analyze_frequency_stability(self, df):
        """Analyze frequency stability and predict issues"""
        
        if df.empty:
            return {}
        
        freq_data = df[['frequency', 'rocof', 'timestamp']].copy()
        freq_data = freq_data.dropna()
        
        if len(freq_data) < 10:
            return {'status': 'insufficient_data'}
        
        # Feature engineering
        features = []
        for _, row in freq_data.iterrows():
            features.append([
                row['frequency'],
                row['rocof'],
                abs(row['frequency'] - 60.0),  # Deviation from nominal
                abs(row['rocof'])               # Absolute ROCOF
            ])
        
        features = np.array(features)
        
        # Fit and predict anomalies
        anomalies = self.models['frequency_anomaly'].fit_predict(features)
        anomaly_scores = self.models['frequency_anomaly'].score_samples(features)
        
        # Calculate statistics
        freq_mean = freq_data['frequency'].mean()
        freq_std = freq_data['frequency'].std()
        rocof_mean = freq_data['rocof'].mean()
        rocof_std = freq_data['rocof'].std()
        
        # Risk assessment
        risk_score = 0
        if abs(freq_mean - 60.0) > 0.1:
            risk_score += 3
        if freq_std > 0.05:
            risk_score += 2
        if abs(rocof_mean) > 0.1:
            risk_score += 2
        if rocof_std > 0.2:
            risk_score += 1
        
        anomaly_count = np.sum(anomalies == -1)
        risk_score += anomaly_count * 0.5
        
        return {
            'status': 'analyzed',
            'frequency_mean': freq_mean,
            'frequency_std': freq_std,
            'rocof_mean': rocof_mean,
            'rocof_std': rocof_std,
            'anomaly_count': anomaly_count,
            'risk_score': min(risk_score, 10),
            'recommendation': self._get_frequency_recommendation(risk_score)
        }
    
    def analyze_voltage_profile(self, df):
        """Analyze voltage profile and unbalance"""
        
        if df.empty:
            return {}
        
        voltage_data = df[['va_mag', 'vb_mag', 'vc_mag', 'timestamp']].copy()
        voltage_data = voltage_data.dropna()
        
        if len(voltage_data) < 10:
            return {'status': 'insufficient_data'}
        
        # Calculate voltage statistics
        va_mean = voltage_data['va_mag'].mean()
        vb_mean = voltage_data['vb_mag'].mean()
        vc_mean = voltage_data['vc_mag'].mean()
        
        # Calculate unbalance
        v_avg = (va_mean + vb_mean + vc_mean) / 3
        unbalance = max(
            abs(va_mean - v_avg),
            abs(vb_mean - v_avg),
            abs(vc_mean - v_avg)
        ) / v_avg * 100
        
        # Feature engineering for anomaly detection
        features = []
        for _, row in voltage_data.iterrows():
            v_avg_row = (row['va_mag'] + row['vb_mag'] + row['vc_mag']) / 3
            features.append([
                row['va_mag'], row['vb_mag'], row['vc_mag'],
                v_avg_row,
                abs(row['va_mag'] - v_avg_row),  # Phase A deviation
                abs(row['vb_mag'] - v_avg_row),  # Phase B deviation
                abs(row['vc_mag'] - v_avg_row)   # Phase C deviation
            ])
        
        features = np.array(features)
        
        # Detect voltage anomalies
        anomalies = self.models['voltage_anomaly'].fit_predict(features)
        anomaly_count = np.sum(anomalies == -1)
        
        # Risk assessment
        risk_score = 0
        if unbalance > 2.0:  # > 2% unbalance
            risk_score += 3
        if any(v < 0.95 or v > 1.05 for v in [va_mean, vb_mean, vc_mean]):
            risk_score += 4
        risk_score += anomaly_count * 0.3
        
        return {
            'status': 'analyzed',
            'va_mean': va_mean,
            'vb_mean': vb_mean, 
            'vc_mean': vc_mean,
            'unbalance_percent': unbalance,
            'anomaly_count': anomaly_count,
            'risk_score': min(risk_score, 10),
            'recommendation': self._get_voltage_recommendation(risk_score, unbalance)
        }
    
    def analyze_power_quality(self, df):
        """Comprehensive power quality analysis"""
        
        if df.empty:
            return {}
        
        # Frequency quality
        freq_analysis = self.analyze_frequency_stability(df)
        
        # Voltage quality
        voltage_analysis = self._analyze_voltage_quality(df)
        
        # Power factor analysis
        pf_analysis = self._analyze_power_factor(df)
        
        # Overall quality score
        quality_score = 10.0
        if freq_analysis.get('risk_score', 0) > 5:
            quality_score -= 3
        if voltage_analysis.get('risk_score', 0) > 5:
            quality_score -= 3
        if pf_analysis.get('risk_score', 0) > 5:
            quality_score -= 2
        
        return {
            'overall_quality_score': max(quality_score, 0),
            'frequency_quality': freq_analysis,
            'voltage_quality': voltage_analysis,
            'power_factor_quality': pf_analysis,
            'recommendations': self._get_overall_recommendations(quality_score)
        }
    
    def predict_system_events(self, df):
        """Predict potential system events using time series patterns"""
        
        if len(df) < 50:
            return {'status': 'insufficient_data'}
        
        # Sort by timestamp
        df_sorted = df.sort_values('timestamp')
        
        # Calculate rolling statistics
        window = 20
        df_sorted['freq_rolling_mean'] = df_sorted['frequency'].rolling(window).mean()
        df_sorted['freq_rolling_std'] = df_sorted['frequency'].rolling(window).std()
        df_sorted['voltage_trend'] = df_sorted['va_mag'].rolling(window).mean().diff()
        
        # Detect trends
        recent_data = df_sorted.tail(30)
        
        predictions = []
        
        # Frequency trend prediction
        freq_trend = recent_data['freq_rolling_mean'].diff().mean()
        if abs(freq_trend) > 0.001:
            severity = min(abs(freq_trend) * 1000, 5)
            predictions.append({
                'event_type': 'frequency_drift',
                'probability': min(abs(freq_trend) * 100, 0.9),
                'severity': severity,
                'description': f"Frequency trending {'up' if freq_trend > 0 else 'down'}"
            })
        
        # Voltage sag prediction
        voltage_trend = recent_data['voltage_trend'].mean()
        if voltage_trend < -0.001:
            predictions.append({
                'event_type': 'voltage_sag',
                'probability': min(abs(voltage_trend) * 50, 0.8),
                'severity': 4,
                'description': "Voltage showing downward trend"
            })
        
        return {
            'status': 'analyzed',
            'predictions': predictions,
            'confidence': 0.7 if len(predictions) > 0 else 0.3
        }
    
    def _analyze_voltage_quality(self, df):
        """Internal voltage quality analysis"""
        
        if df.empty:
            return {'risk_score': 0}
        
        voltage_data = df[['va_mag', 'vb_mag', 'vc_mag']].mean()
        
        risk_score = 0
        for v in voltage_data:
            if v < 0.95 or v > 1.05:  # ±5% tolerance
                risk_score += 2
        
        return {'risk_score': min(risk_score, 10)}
    
    def _analyze_power_factor(self, df):
        """Analyze power factor from phasor data"""
        
        if df.empty:
            return {'risk_score': 0}
        
        # Calculate power factor from voltage and current angles
        pf_data = []
        for _, row in df.iterrows():
            try:
                # Simplified power factor calculation
                v_angle = row['va_angle'] if 'va_angle' in row else 0
                i_angle = row['i1_angle'] if 'i1_angle' in row else 0
                pf = abs(np.cos(np.radians(v_angle - i_angle)))
                pf_data.append(pf)
            except:
                continue
        
        if not pf_data:
            return {'risk_score': 0}
        
        avg_pf = np.mean(pf_data)
        risk_score = 0
        
        if avg_pf < 0.85:  # Poor power factor
            risk_score = 5
        elif avg_pf < 0.9:  # Fair power factor
            risk_score = 2
        
        return {
            'average_power_factor': avg_pf,
            'risk_score': risk_score
        }
    
    def _get_frequency_recommendation(self, risk_score):
        """Get recommendation based on frequency risk score"""
        
        if risk_score > 7:
            return "CRITICAL: Immediate frequency regulation required"
        elif risk_score > 5:
            return "HIGH: Monitor frequency closely, consider load shedding"
        elif risk_score > 3:
            return "MEDIUM: Increase monitoring frequency"
        else:
            return "LOW: Normal frequency operation"
    
    def _get_voltage_recommendation(self, risk_score, unbalance):
        """Get recommendation based on voltage analysis"""
        
        if risk_score > 7:
            return "CRITICAL: Voltage regulation required immediately"
        elif unbalance > 3.0:
            return "HIGH: Significant voltage unbalance detected"
        elif risk_score > 3:
            return "MEDIUM: Monitor voltage profile"
        else:
            return "LOW: Normal voltage operation"
    
    def _get_overall_recommendations(self, quality_score):
        """Get overall system recommendations"""
        
        recommendations = []
        
        if quality_score < 4:
            recommendations.append("URGENT: Multiple power quality issues detected")
            recommendations.append("Consider immediate corrective actions")
        elif quality_score < 7:
            recommendations.append("CAUTION: Power quality degrading")
            recommendations.append("Schedule maintenance check")
        else:
            recommendations.append("GOOD: System operating within normal parameters")
        
        return recommendations
    
    def generate_report(self, hours_back=1):
        """Generate comprehensive ML analysis report"""
        
        print(f"🤖 ML Analysis Report - Last {hours_back} hour(s)")
        print("="*60)
        
        # Load data
        df = self.load_data(hours_back)
        
        if df.empty:
            print("❌ No data available for analysis")
            return
        
        print(f"📊 Analyzed {len(df)} measurements from {len(df['pmu_id'].unique())} PMUs")
        print(f"⏰ Time range: {datetime.fromtimestamp(df['timestamp'].min())}")
        print(f"            to {datetime.fromtimestamp(df['timestamp'].max())}")
        
        # Frequency analysis
        print("\n⚡ FREQUENCY ANALYSIS:")
        freq_analysis = self.analyze_frequency_stability(df)
        if freq_analysis.get('status') == 'analyzed':
            print(f"  Mean Frequency: {freq_analysis['frequency_mean']:.3f} Hz")
            print(f"  Std Deviation: {freq_analysis['frequency_std']:.4f} Hz")
            print(f"  ROCOF Mean: {freq_analysis['rocof_mean']:.3f} Hz/s")
            print(f"  Anomalies: {freq_analysis['anomaly_count']}")
            print(f"  Risk Score: {freq_analysis['risk_score']:.1f}/10")
            print(f"  📋 {freq_analysis['recommendation']}")
        
        # Voltage analysis
        print("\n🔋 VOLTAGE ANALYSIS:")
        voltage_analysis = self.analyze_voltage_profile(df)
        if voltage_analysis.get('status') == 'analyzed':
            print(f"  VA: {voltage_analysis['va_mean']:.3f} kV")
            print(f"  VB: {voltage_analysis['vb_mean']:.3f} kV") 
            print(f"  VC: {voltage_analysis['vc_mean']:.3f} kV")
            print(f"  Unbalance: {voltage_analysis['unbalance_percent']:.2f}%")
            print(f"  Risk Score: {voltage_analysis['risk_score']:.1f}/10")
            print(f"  📋 {voltage_analysis['recommendation']}")
        
        # Power quality analysis
        print("\n⚙️  POWER QUALITY ANALYSIS:")
        pq_analysis = self.analyze_power_quality(df)
        if pq_analysis:
            print(f"  Overall Quality Score: {pq_analysis['overall_quality_score']:.1f}/10")
            for rec in pq_analysis.get('recommendations', []):
                print(f"  📋 {rec}")
        
        # Event prediction
        print("\n🔮 EVENT PREDICTION:")
        predictions = self.predict_system_events(df)
        if predictions.get('status') == 'analyzed':
            if predictions['predictions']:
                for pred in predictions['predictions']:
                    print(f"  🚨 {pred['event_type'].upper()}: {pred['probability']:.1%} probability")
                    print(f"     Severity: {pred['severity']}/5 - {pred['description']}")
            else:
                print("  ✅ No immediate events predicted")
        
        print("\n" + "="*60)

def main():
    """Main function for ML analysis"""
    
    import sys
    
    hours_back = 1
    if len(sys.argv) > 1:
        try:
            hours_back = float(sys.argv[1])
        except ValueError:
            print("Usage: python3 ml_analyzer.py [hours_back]")
            return
    
    analyzer = SynchrophasorMLAnalyzer()
    analyzer.generate_report(hours_back)

if __name__ == "__main__":
    main() 