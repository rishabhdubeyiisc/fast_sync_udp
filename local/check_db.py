#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('synchrophasor_data.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM measurements')
measurements = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM system_events')
events = cursor.fetchone()[0]

print('📊 Enhanced Synchrophasor Database Summary:')
print(f'   💾 Measurements: {measurements}')
print(f'   🚨 Events: {events}')

if measurements > 0:
    cursor.execute('SELECT DISTINCT pmu_id FROM measurements')
    pmus = [str(p[0]) for p in cursor.fetchall()]
    print(f'   🏭 PMUs: {", ".join(pmus)}')
    
    cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM measurements')
    times = cursor.fetchone()
    if times[0]:
        duration = (times[1] - times[0]) / 60
        print(f'   ⏰ Data span: {duration:.1f} minutes')
        
    cursor.execute('SELECT frequency, va_mag FROM measurements ORDER BY timestamp DESC LIMIT 3')
    recent = cursor.fetchall()
    print(f'   📈 Recent data samples: {len(recent)}')

conn.close() 