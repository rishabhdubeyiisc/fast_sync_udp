from struct import pack as struct_pack

# table for calculating CRC
# this particular table was generated using pycrc v0.7.6, http://www.tty1.net/pycrc/
# using the configuration:
#  *    Width        = 16
#  *    Poly         = 0x1021
#  *    XorIn        = 0x0000
#  *    ReflectIn    = False
#  *    XorOut       = 0x0000
#  *    ReflectOut   = False
#  *    Algorithm    = table-driven
# by following command:
#   python pycrc.py --model xmodem --algorithm table-driven --generate c

CRC16_XMODEM_TABLE = [
    0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
    0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
    0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
    0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
    0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
    0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
    0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
    0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
    0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
    0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
    0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
    0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
    0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
    0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
    0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
    0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
    0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
    0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
    0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
    0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
    0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
    0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
    0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
    0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
    0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
    0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
    0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
    0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
    0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
    0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
    0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
    0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0,
]

FRAME_TYPES_STR_TO_NUM    = { "data" : 0, "header" : 1, "cfg1" : 2, "cfg2" : 3 , "cmd" : 4 ,"cfg3" : 5  }

FRAME_TYPES_NUM_TO_STR    = { 0 : "data", 1: "header" , 2: "cfg1" , 3 : "cfg2" , 4 : "cmd" , 5 : "cfg3" }

def _crc16(data, crc, table):
    """Calculate CRC16 using the given table.
    `data`      - data for calculating CRC, must be bytes
    `crc`       - initial value
    `table`     - table for calculating CRC (list of 256 integers)
    Return calculated value of CRC
    """
    for byte in data:
        crc = ((crc << 8) & 0xff00) ^ table[((crc >> 8) & 0xff) ^ byte]
    return crc & 0xffff

def crc16xmodem(data, crc=0):
    """Calculate CRC-CCITT (XModem) variant of CRC16.
    `data`      - data for calculating CRC, must be bytes
    `crc`       - initial value
    Return calculated value of CRC
    """
    return _crc16(data, crc, CRC16_XMODEM_TABLE)

def _check_crc(byte_data):
    crc_calculated = crc16xmodem(byte_data[0:-2], 0xffff).to_bytes(2, "big")  # Calculate CRC
    if byte_data[-2:] != crc_calculated:
        return False
    return True

def extract_frame_type(byte_data):
    '''
        ASAP extract frame type and check CRC 
        then create class instance
    '''

    # Check if frame is valid
    if not _check_crc(byte_data):
        raise FrameError("CRC failed. Frame not valid.")

    # Get second byte and determine frame type by shifting right to get higher 4 bits
    frame_type_num = int.from_bytes([byte_data[1]], byteorder="big", signed=False) >> 4

    return FRAME_TYPES_NUM_TO_STR[frame_type_num]

class CommonFrame():
    def __init__(   self , 
                    frame_type : str = 'data',
                    pmu_id_code: int = 123,
                    soc        : int = 0,
                    fracsec    : int = 0,
                    version    : int = 1 
                    ):
        self.set_frame_type(frame_type_str = frame_type)
    
    def set_frame_type(self, frame_type_str : str = 'data'):
        if frame_type not in self.FRAME_TYPES_STR_TO_NUM :
            raise FrameError("Unknown frame type. Possible options: [data, header, cfg1, cfg2, cfg3, cmd].")
        else:
            self._frame_type_num = self.FRAME_TYPES_STR_TO_NUM[frame_type_str]

    def get_frame_type(self):
        return self._frame_type_num

    def set_version(self, version):
        '''
            set version only 4 bits allowed to enter
        '''
        if not 1 <= version <= 15:
            raise FrameError("VERSION number out of range. 1<= VERSION <= 15")
        else:
            self._version = version

    def get_version(self):
        return self._version

    def set_id_code(self, id_code):
    '''
    * ``id_code`` **(int)** - Should be number between ``1`` and ``65534``.
    '''
    if not 1 <= id_code <= 65534:
        raise FrameError("ID CODE out of range. 1 <= ID_CODE <= 65534")
    else:
        self._pmu_id_code = id_code

    def get_id_code(self):
        return self._pmu_id_code

    def set_time(self, soc=None, frasec=None):
        '''
        soc , frasec : int if not given will be set by function 
        based on current time
        '''

        t = time()  # Get current timestamp

        if soc:
            self.set_soc(soc)
        else:
            self.set_soc(int(t))  # Get current timestamp

        if frasec:
            self.set_frasec(frasec)  # Just set fraction of second and use default values for other arguments.
        else:
            #24 bit allowed
            self.set_frasec(int ( ( t - int(t) ) * (10 ** 6) ) ) 


    def set_soc(self, soc):
        '''
        provide current soc value shoule be less than 2 ** 32 - 1
        '''
        if not 0 <= soc <= 4294967295:
            raise FrameError("Time stamp out of range. 0 <= SOC <= 4294967295")
        else:
            self._soc = soc



class FrameError(BaseException):
    pass















































def frame_data_build(
             SYNC       : int = 0xAA01, 
             FRAME_SIZE : int = 52, 
             IDCODE     : int = 7734, 
             SOC        : int = 0x00000000, 
             FRACSEC    : int = 0x00000000,
             STAT       : int = 0,
             PHASOR_VA  : int = 0x392B0000, 
             PHASOR_VB  : int = 0xE36ACE7C, 
             PHASOR_VC  : int = 0xE36A3183, 
             PHASOR_IA  : int = 0x04440000, 
             FREQ       : int = 0x09C4,
             DFREQ      : int = 0,
             ANALOG1    : int = 0x42C80000,
             ANALOG2    : int = 0x447A0000,
             ANALOG3    : int = 0x461C4000,
             DIGITAL    : int = 0x3C12 ,
             CHK        : int = 0xD43F) -> bytes:
    '''
    SYNC       :  2, 
    FRAME_SIZE :  2, 
    IDCODE     :  2, 
    SOC        :  4, 
    FRACSEC    :  4,
    STAT       :  2,
    PHASOR_VA  :  4, 
    PHASOR_VB  :  4, 
    PHASOR_VC  :  4, 
    PHASOR_IA  :  4, 
    FREQ       :  2,
    DFREQ      :  2,
    ANALOG1    :  4,
    ANALOG2    :  4,
    ANALOG3    :  4,
    DIGITAL    :  2,
    CHK        :  2  
    '''

    pack_sequence = '!HHHIIHIIIIHHIIIHH'
    packet = struct_pack(   pack_sequence       ,
                            SYNC                , 
                            FRAME_SIZE          ,
                            IDCODE              ,
                            SOC                 ,
                            FRACSEC             ,
                            STAT                ,
                            PHASOR_VA           ,
                            PHASOR_VB           ,
                            PHASOR_VC           ,
                            PHASOR_IA           ,
                            FREQ                ,
                            DFREQ               ,
                            ANALOG1             ,
                            ANALOG2             ,
                            ANALOG3             ,
                            DIGITAL             ,
                            CHK                 
                        )
    return packet

x = frame_data_build()
i = _check_crc(x)