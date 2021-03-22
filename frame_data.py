FRAME_TYPES_STR_TO_NUM    = { "data" : 0, "header" : 1, "cfg1" : 2, "cfg2" : 3 , "cmd" : 4 ,"cfg3" : 5  }

FRAME_TYPES_NUM_TO_STR    = { 0 : "data", 1: "header" , 2: "cfg1" , 3 : "cfg2" , 4 : "cmd" , 5 : "cfg3" }

MAX_23_Bit = (2**23-1)

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

def extract_frame_type(byte_data)->str:
    """This method will only return type of the frame. It shall be used for stream splitter
    since there is no need to create instance of specific frame which will cause lower performance."""

    # Check if frame is valid
    if not CommandFrame._check_crc(byte_data):
        raise FrameError("CRC failed. Frame not valid.")

    # Get second byte and determine frame type by shifting right to get higher 4 bits
    frame_type = int.from_bytes([byte_data[1]], byteorder="big", signed=False) >> 4

    return FRAME_TYPES_NUM_TO_STR[frame_type]

class CommonFrame(object):
    def __init__(self,
                frame_type      : str = 'data'  ,
                ieee_version    : int = 1       ,
                id_code         : int = 123     ,
                soc             : int = 0       ,
                fracsec         : int = 0              
                ):
        self.set_frame_type(frame_type)
        self.set_version(ieee_version)
        self.set_id_code(id_code)

        if soc or frasec:
            self.set_time(soc = soc, frasec = fracsec)

    def set_frame_type(self ,frame_type : str = 'data'):
        if frame_type not in FRAME_TYPES_STR_TO_NUM :
            raise FrameError("Unknown frame type. Possible options: [data, header, cfg1, cfg2, cfg3, cmd].")
        else:
            self._frame_type_num = FRAME_TYPES_STR_TO_NUM[frame_type]

    def get_frame_type(self)-> int :
        return self._frame_type_num

    def set_version(self , ieee_version : int = 1):
        '''
            set version only 4 bits allowed to enter
        '''
        if not 1 <= ieee_version <= 15:
            raise FrameError("VERSION number out of range. 1<= VERSION <= 15")
        else:
            self._version = ieee_version
    
    def get_version(self)->int:
        return self._version

    def set_id_code(self, id_code : int ):
        '''
        * ``id_code`` **(int)** - Should be number between ``1`` and ``65534``.
        '''
        if not 1 <= id_code <= 65534:
            raise FrameError("ID CODE out of range. 1 <= ID_CODE <= 65534")
        else:
            self._pmu_id_code = id_code

    def get_id_code(self)-> int :
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

    def get_soc(self):
        return self._soc

    def set_frasec(self, fr_seconds     : int   = 0     , 
                         leap_dir       : str   = "+"   , 
                         leap_occ       : bool  = False , 
                         leap_pen       : bool  = False , 
                         time_quality   : int   = 7 
                  ):
        """
        **Params:**
        *    ``leap_dir`` **(char)** - Leap Second Direction: ``+`` for add (``0``), ``-`` for
             delete (``1``).
             Default value: ``+``.
        *    ``leap_occ`` **(bool)** - Leap Second Occurred: ``True`` in the first second after
             the leap second occurs and remains set for 24h.
        *    ``leap_pen`` **(bool)** - Leap Second Pending: ``True`` not more than 60 s nor less
             than 1 s before a leap second occurs, and cleared in the second after the leap
             second occurs.
        *    ``time_quality`` **(int)** - Message Time Quality represents worst-case clock
             accuracy according to UTC. Table below shows code values. Should be between ``0``
             and ``15``.
        __________________________________________________________________________________________
            +------------+----------+---------------------------+
            |  Binary    |  Decimal |           Value           |
            +------------+----------+---------------------------+
            | 1111       |    15    | Fault - clock failure.    |
            +------------+----------+---------------------------+
            | 1011       |    11    | Time within 10s of UTC.   |
            +------------+----------+---------------------------+
            | 1010       |    10    | Time within 1s of UTC.    |
            +------------+----------+---------------------------+
            | 1001       |    9     | Time within 10^-1s of UTC.|
            +------------+----------+---------------------------+
            | 1000       |    8     | Time within 10^-2s of UTC.|
            +------------+----------+---------------------------+
            | 0111       |    7     | Time within 10^-3s of UTC.|
            +------------+----------+---------------------------+
            | 0110       |    6     | Time within 10^-4s of UTC.|
            +------------+----------+---------------------------+
            | 0101       |    5     | Time within 10^-5s of UTC.|
            +------------+----------+---------------------------+
            | 0100       |    4     | Time within 10^-6s of UTC.|
            +------------+----------+---------------------------+
            | 0011       |    3     | Time within 10^-7s of UTC.|
            +------------+----------+---------------------------+
            | 0010       |    2     | Time within 10^-8s of UTC.|
            +------------+----------+---------------------------+
            | 0001       |    1     | Time within 10^-9s of UTC.|
            +------------+----------+---------------------------+
            | 0000       |    0     | Clock locked to UTC.      |
            +------------+----------+---------------------------+
        """

        if not 0 <= fr_seconds <= 16777215:
            raise FrameError("Frasec out of range. 0 <= FRASEC <= 16777215 ")

        if (not 0 <= time_quality <= 15) or (time_quality in [12, 13, 14]):
            raise FrameError("Time quality flag out of range. 0 <= MSG_TQ <= 15")

        if leap_dir not in ["+", "-"]:
            raise FrameError("Leap second direction must be '+' or '-'")

        frasec = 1 << 1  # Bit 7: Reserved for future use. Not important but it will be 1 for easier byte forming.

        if leap_dir == "-":  # Bit 6: Leap second direction [+ = 0] and [- = 1].
            frasec |= 1

        frasec <<= 1

        if leap_occ:  # Bit 5: Leap Second Occurred, 1 in first second after leap second, remains 24h.
            frasec |= 1

        frasec <<= 1

        if leap_pen:  # Bit 4: Leap Second Pending - shall be 1 not more then 60s nor less than 1s before leap second.
            frasec |= 1

        frasec <<= 4  # Shift left 4 bits for message time quality

        # Bit 3 - 0: Message Time Quality indicator code - integer representation of bits (check table).
        frasec |= time_quality

        mask = 1 << 7  # Change MSB to 0 for standard compliance.
        frasec ^= mask

        frasec <<= 24  # Shift 24 bits for fractional time.

        frasec |= fr_seconds  # Bits 23-0: Fraction of second.

        self._frasec = frasec

    def get_frasec(self):
        '''
        return fr_seconds, leap_dir, leap_occ, leap_pen, time_quality = (int , str , bool , bool , int)
        '''
        return _int2frasec(self._frasec)
    
    def build(self , byte_message : bytes = "start".encode('utf-8') ):
        return self.convert2bytes(byte_message=byte_message)
    
    @staticmethod
    def _int2frasec(frasec_int) -> (int , str , bool , bool , int):

        tq = frasec_int >> 24
        leap_dir = tq & 0b01000000
        leap_occ = tq & 0b00100000
        leap_pen = tq & 0b00010000

        time_quality = tq & 0b00001111

        # Reassign values to create Command frame
        leap_dir = "-" if leap_dir else "+"
        leap_occ = bool(leap_occ)
        leap_pen = bool(leap_pen)

        fr_seconds = frasec_int & MAX_23_Bit

        return fr_seconds, leap_dir, leap_occ, leap_pen, time_quality
    
    @staticmethod
    def _check_crc(byte_data):

        crc_calculated = crc16xmodem(byte_data[0:-2], 0xffff).to_bytes(2, "big")  # Calculate CRC

        if byte_data[-2:] != crc_calculated:
            return False

        return True
    
    def convert2bytes(self, byte_message):

        # SYNC word in CommonFrame starting with AA hex word + frame type + version
        sync_b = (0xaa << 8) | (self._frame_type_num << 4) | self._version
        sync_b = sync_b.to_bytes(2, "big")

        # FRAMESIZE: 2B SYNC + 2B FRAMESIZE + 2B IDCODE + 4B SOC + 4B FRASEC + len(Command) + 2B CHK
        frame_size_b = (16 + len(byte_message)).to_bytes(2, "big")

        # PMU ID CODE
        pmu_id_code_b = self._pmu_id_code.to_bytes(2, "big")

        # If timestamp not given set timestamp
        if not hasattr(self, "_soc") and not hasattr(self, "_frasec"):
            self.set_time()
        elif not self._soc and not self._frasec:
            self.set_time()

        # SOC
        soc_b = self._soc.to_bytes(4, "big")

        # FRASEC
        frasec_b = self._frasec.to_bytes(4, "big")

        # CHK
        crc_chk_b = crc16xmodem(sync_b + frame_size_b + pmu_id_code_b + soc_b + frasec_b + byte_message, 0xffff)

        return sync_b + frame_size_b + pmu_id_code_b + soc_b + frasec_b + byte_message + crc_chk_b.to_bytes(2, "big")



class ConfigFrame1(CommonFrame):
    """
    ## ConfigFrame1 ##

    ConfigFrame1 is class which represents configuration frame v1.
    Configuration frame version 1 carries info about device reporting
    ability.

    Class implements two abstract methods from super class.

    * ``convert2bytes()`` - for converting ConfigFrame1 to bytes.
    * ``convert2frame()`` - which converts array of bytes to ConfigFrame1.

    Each instance of ConfigFrame1 class will have following attributes.

    **Attributes:**

    * ``frame_type`` **(int)** - Defines frame type. Inherited from ``CommonFrame``.
    * ``version`` **(int)** - Standard version. Inherited from ``CommonFrame``. Default value: ``1``.
    * ``pmu_id_code`` **(int)** - PMU Id code which identifies data stream. Inherited from ``CommonFrame``.
    * ``soc`` **(int)** - UNIX timestamp. Default value: ``None``. Inherited from ``CommonFrame``.
    * ``frasec`` **(int)** - Fraction of second and Time Quality. Default value: ``None``.
      Inherited from ``CommonFrame``.
    * ``time_base`` **(int)** - Resolution of the fractional second time stamp in all frames.
    * ``num_pmu`` **(int)** - Number of PMUs (data streams) included in single ``DataFrame``.
    * ``multistreaming`` **(bool)** - ``True`` if ``num_pmu > 1``. That means data frame consist of multiple
      measurement streams.
    * ``station_name`` **(mixed)** - Station name ``(string)`` or station names ``(list)`` if ``multistreaming``.
    * ``id_code`` **(mixed)** - Measurement stream ID code ``(int)`` or ``(list)`` if ``multistreaming``. Each ID
      identifies source PMU of each data block.
    * ``data_format`` **(mixed)** - Data format for each data stream. Inherited from ``CommonFrame``.
    * ``phasor_num`` **(mixed)** - Number of phasors ``(int)`` or ``(list)`` if ``multistreaming``.
    * ``analog_num`` **(mixed)** - Number of analog values ``(int)`` or ``(list)`` if ``multistreaming``.
    * ``digital_num`` **(mixed)** - Number of digital status words ``(int)`` or ``(list)`` if ``multistreaming``.
    * ``channel_names`` **(list)** - List of phasor and channel names for phasor, analog and digital channel.
      If ``multistreaming`` it's list of lists.
    * ``ph_units`` **(list)** - Conversion factor for phasor channels. If ``multistreaming`` list of lists.
    * ``an_units`` **(list)** - Conversion factor for analog channels. If ``multistreaming`` list of lists.
    * ``dig_units`` **(list)** - Mask words for digital status word. If ``multistreaming`` list of lists.
    * ``fnom``  **(mixed)** - Nominal frequency code and flags. If ``multistreaming`` list of ints.
    * ``cfg_count`` **(mixed)** - Configuration change count. If ``multistreaming`` list of ints.
    * ``data_rate`` **(int)** - Frames per second or seconds per frame (if negative ``int``).

    **Raises:**

        FrameError
    When it's not possible to create valid frame, usually due invalid parameter value.
    """

    def __init__(self, pmu_id_code : int , time_base, num_pmu, station_name, id_code, data_format, phasor_num, analog_num,
                 digital_num, channel_names, ph_units, an_units, dig_units, f_nom, cfg_count, data_rate,
                 soc=None, frasec=None, version : int =1):

        super().__init__(frame_type = "cfg1", id_code = pmu_id_code, soc = soc, fracsec = frasec, ieee_version = version)  # Init CommonFrame with 'cfg1' frame type
        
        self.set_time_base(time_base)
        self.set_num_pmu(num_pmu)
        self.set_stn_names(station_name)
        self.set_stream_id_code(id_code)
        self.set_data_format(data_format, num_pmu)
        self.set_phasor_num(phasor_num)
        self.set_analog_num(analog_num)
        self.set_digital_num(digital_num)
        self.set_channel_names(channel_names)
        self.set_phasor_units(ph_units)
        self.set_analog_units(an_units)
        self.set_digital_units(dig_units)
        self.set_fnom(f_nom)
        self.set_cfg_count(cfg_count)
        self.set_data_rate(data_rate)


    def set_time_base(self, time_base):
        """
        ### set_time_base() ###

        Setter for time base. Resolution of the fractional second time stamp (FRASEC).
        Bits 31-24: Reserved for flags (high 8 bits).
        Bits 23-0: 24-bit unsigned integer which subdivision of the second that the FRASEC
        is based on.

        **Params:**

        * ``time_base`` **(int)** - Should be number between ``1`` and ``16777215``.

        **Raises:**

            FrameError
        When ``time_base`` value provided is out of range.

        """

        if not 1 <= time_base <= 16777215:
            raise FrameError("Time Base out of range. 1 <= TIME_BASE <= 16777215 ")
        else:
            self._time_base = time_base


    def get_time_base(self):

        return self._time_base


    def set_num_pmu(self, num_pmu):
        """
        ### set_num_pmu() ###

        Setter for number of PMUs. The number of PMUs included in data frame. No limit
        specified. The actual limit will be determined by the limit of 65 535 bytes in one
        frame (FRAMESIZE filed).

        Also, if ``num_pmu`` > ``1`` multistreaming will be set to ``True`` meaning that
        more then one data stream will be sent inside data frame.

        **Params:**

        * ``num_pmu`` **(int)** - Should be number between ``1`` and ``65535``.

        **Raises:**

            FrameError
        When ``num_pmu`` value provided is out of range.

        """

        if not 1 <= num_pmu <= 65535:
            raise FrameError("Number of PMUs out of range. 1 <= NUM_PMU <= 65535")
        else:
            self._num_pmu = num_pmu
            self._multistreaming = True if num_pmu > 1 else False


    def get_num_pmu(self):

        return self._num_pmu


    def is_multistreaming(self):

        return self._multistreaming


    def set_stn_names(self, station_name):
        """
        ### set_stn_names() ###

        Setter for station names.

        If ``multistreaming`` should be list of ``num_pmu`` station names otherwise 16
        character ASCII string.

        **Params:**

        * ``station_name`` **(mixed)** - Should be 16 bytes (16 ASCII characters) string
        or list of strings.

        **Raises:**

            FrameError
        When ``station_name`` is not list with length ``num_pmu`` when ``multistreaming``.

        """

        if self._multistreaming:
            if not isinstance(station_name, list) or self._num_pmu != len(station_name):
                raise FrameError("When NUM_PMU > 1 provide station names as list with NUM_PMU elements.")

            self._station_name = [station[:16].ljust(16, " ") for station in station_name]
        else:
            self._station_name = station_name[:16].ljust(16, " ")


    def get_station_name(self):

        return self._station_name


    def set_stream_id_code(self, id_code):
        """
        ### set_config_id_code() ###

        Setter for data stream IDs inside data frame.

        If ``multistreaming`` should be
        a list of IDs otherwise should be same as ``pmu_id_code``.

        **Params:**

        * ``id_code`` **(mixed)** - Should be number between ``1`` and ``65534``.
        If ``multistreaming`` list of numbers.

        **Raises:**

            FrameError
        When ``id_code`` is not list with length ``num_pmu`` when ``multistreaming``.
        When ``id_code`` value is out of range.

        """

        if self._multistreaming:
            if not isinstance(id_code, list) or self._num_pmu != len(id_code):
                raise FrameError("When NUM_PMU > 1 provide PMU ID codes as list with NUM_PMU elements.")

            for stream_id in id_code:
                if not 1 <= stream_id <= 65534:
                    raise FrameError("ID CODE out of range. 1 <= ID_CODE <= 65534")
        else:
            if not 1 <= id_code <= 65534:
                raise FrameError("ID CODE out of range. 1 <= ID_CODE <= 65534")

        self._id_code = id_code


    def get_stream_id_code(self):

        return self._id_code


    def set_phasor_num(self, phasor_num):
        """
        ### set_phasor_num() ###

        Setter for number of phasor measurements. Should be specified for each
        data stream in data frame.

        If ``multistreaming`` should be a list of ``integers`` otherwise should be ``integer``.

        **Params:**

        * ``phasor_num`` **(mixed)** - Should be integer between ``1`` and ``65535``.
        If ``multistreaming`` list of numbers.

        **Raises:**

            FrameError
        When ``phasor_num`` is not list with length ``num_pmu`` when ``multistreaming``.
        When ``phasor_num`` value is out of range.

        """

        if self._multistreaming:
            if not isinstance(phasor_num, list) or self._num_pmu != len(phasor_num):
                raise FrameError("When NUM_PMU > 1 provide PHNMR as list with NUM_PMU elements.")

            for phnmr in phasor_num:
                if not 0 <= phnmr <= 65535:
                    raise FrameError("Number of phasors out of range. 0 <= PHNMR <= 65535")
        else:
            if not 0 <= phasor_num <= 65535:
                raise FrameError("Number of phasors out of range. 0 <= PHNMR <= 65535")

        self._phasor_num = phasor_num


    def get_phasor_num(self):

        return self._phasor_num


    def set_analog_num(self, analog_num):
        """
        ### set_analog_num() ###

        Setter for number analog values. Should be specified for each
        data stream in data frame.

        If ``multistreaming`` should be a list of ``integers`` otherwise should be ``integer``.

        **Params:**

        * ``analog_num`` **(mixed)** - Should be integer between ``1`` and ``65535``.
        If ``multistreaming`` list of numbers.

        **Raises:**

            FrameError
        When ``analog_num`` is not list with length ``num_pmu`` when ``multistreaming``.
        When ``analog_num`` value is out of range.

        """

        if self._multistreaming:
            if not isinstance(analog_num, list) or self._num_pmu != len(analog_num):
                raise FrameError("When NUM_PMU > 1 provide ANNMR as list with NUM_PMU elements.")

            for annmr in analog_num:
                if not 0 <= annmr <= 65535:
                    raise FrameError("Number of phasors out of range. 0 <= ANNMR <= 65535")
        else:
            if not 0 <= analog_num <= 65535:
                raise FrameError("Number of phasors out of range. 0 <= ANNMR <= 65535")

        self._analog_num = analog_num


    def get_analog_num(self):

        return self._analog_num


    def set_digital_num(self, digital_num):
        """
        ### set_digital_num() ###

        Setter for number of digital status words. Should be specified for each
        data stream in data frame.

        If ``multistreaming`` should be a list of ``integers`` otherwise should be ``integer``.

        **Params:**

        * ``digital_num`` **(mixed)** - Should be integer between ``1`` and ``65535``.
        If ``multistreaming`` list of numbers.

        **Raises:**

            FrameError
        When ``digital_num`` is not list with length ``num_pmu`` when ``multistreaming``.
        When ``digital_num`` value is out of range.

        """
        if self._multistreaming:
            if not isinstance(digital_num, list) or self._num_pmu != len(digital_num):
                raise FrameError("When NUM_PMU > 1 provide DGNMR as list with NUM_PMU elements.")

            for dgnmr in digital_num:
                if not 0 <= dgnmr <= 65535:
                    raise FrameError("Number of phasors out of range. 0 <= DGNMR <= 65535")
        else:
            if not 0 <= digital_num <= 65535:
                raise FrameError("Number of phasors out of range. 0 <= DGNMR <= 65535")

        self._digital_num = digital_num


    def get_digital_num(self):

        return self._digital_num


    def set_channel_names(self, channel_names):
        """
        ### set_channel_names() ###

        Setter for phasor and channel names.

        **Params:**

        * ``channel_names`` **(list)** - Should be list of strings (16 ASCII character) with
        ``PHASOR_NUM`` + ``ANALOG_NUM`` + 16 * ``DIGITAL_NUM`` elements.
        If ``multistreaming`` should be list of lists.

        **Raises:**

            FrameError
        When ``channel_names`` is not list of lists with length ``num_pmu`` when ``multistreaming``.
        When ``channel_names`` is not list with ``PHASOR_NUM`` + ``ANALOG_NUM`` +
        + 16 * ``DIGITAL_NUM`` elements.

        """

        if self._multistreaming:
            if not all(isinstance(el, list) for el in channel_names) or self._num_pmu != len(channel_names):
                raise FrameError("When NUM_PMU > 1 provide CHNAM as list of lists with NUM_PMU elements.")

            channel_name_list = []
            for i, chnam in enumerate(channel_names):
                # Channel names must be list with PHNMR + ANNMR + 16*DGNMR elements. Each bit in one digital word
                # (16bit) has it's own label.
                if (self._phasor_num[i] + self._analog_num[i] + 16 * self._digital_num[i]) != len(chnam):
                    raise FrameError("Provide CHNAM as list with PHNMR + ANNMR + 16*DGNMR elements for each stream.")
                channel_name_list.append([chn[:16].ljust(16, " ") for chn in chnam])

            self._channel_names = channel_name_list
        else:
            if not isinstance(channel_names, list) or \
                            (self._phasor_num + self._analog_num + 16 * self._digital_num) != len(channel_names):
                raise FrameError("Provide CHNAM as list with PHNMR + ANNMR + 16*DGNMR elements.")

            self._channel_names = [channel[:16].ljust(16, " ") for channel in channel_names]


    def get_channel_names(self):

        return self._channel_names


    def set_phasor_units(self, ph_units):
        """
        ### set_phasor_units() ###

        Setter for phasor channels conversion factor.

        **Params:**

        * ``ph_units`` **(list)** - Should be list of tuples ``(scale, phasor_type)``
        where phasor type is ``'i'`` for current and ``'v'`` for voltage.
        If ``multistreaming`` should be list of lists.

        **Raises:**

            FrameError
        When ``ph_units`` is not list of lists with length ``num_pmu`` when ``multistreaming``.
        When ``ph_units`` element is not tuple.

        """

        if self._multistreaming:
            if not all(isinstance(el, list) for el in ph_units) or self._num_pmu != len(ph_units):
                raise FrameError("When NUM_PMU > 1 provide PHUNIT as list of lists.")

            phunit_list = []
            for i, ph_unit in enumerate(ph_units):
                if not all(isinstance(el, tuple) for el in ph_unit) or self._phasor_num[i] != len(ph_unit):
                    raise FrameError("Provide PHUNIT as list of tuples with PHNMR elements. "
                                     "Ex: [(1234,'u'),(1234, 'i')]")

                ph_values = []
                for ph_tuple in ph_unit:
                    ph_values.append(ConfigFrame1._phunit2int(*ph_tuple))

                phunit_list.append(ph_values)

            self._ph_units = phunit_list
        else:
            if not all(isinstance(el, tuple) for el in ph_units) or self._phasor_num != len(ph_units):
                raise FrameError("Provide PHUNIT as list of tuples with PHNMR elements. Ex: [(1234,'u'),(1234, 'i')]")

            self._ph_units = [ConfigFrame1._phunit2int(*phun) for phun in ph_units]


    def get_ph_units(self):

        if all(isinstance(el, list) for el in self._ph_units):
            return [[self._int2phunit(unit) for unit in ph_units] for ph_units in self._ph_units]
        else:
            return [self._int2phunit(ph_unit) for ph_unit in self._ph_units]


    @staticmethod
    def _phunit2int(scale, phasor_type="v"):
        """
        ### phunit2int() ###

        Convert method for phasor channels conversion factor.

        MSB: If phasor type is ``v`` then MSB will be ``0``.
        If phasor type is ``i`` then MSB will be ``1``.

        LSB: Unsigned 24 bit word in 10^-5 V or amperes per bit
        to scale 16-bit integer data.

        If transmitted data is in floating-point format, LSB 24 bit value
        shall be ignored.

        **Params:**

        * ``scale`` **(int)** - scale factor.
        * ``phasor_type`` **(char)** - ``v`` - voltage, ``i`` - current.
        Default value: ``v``.

        **Returns:**

        * ``int`` which represents phasor channels conversion factor.

        **Raises:**

            FrameError
        When ``scale`` is out of range.

        """

        if not 0 <= scale <= 16777215:
            raise ValueError("PHUNIT scale out of range. 0 <= PHUNIT <= 16777215.")

        if phasor_type not in ["v", "i"]:
            raise ValueError("Phasor type should be 'v' or 'i'.")

        if phasor_type == "i":
            phunit = 1 << 24
            return phunit | scale
        else:
            return scale


    @staticmethod
    def _int2phunit(ph_unit):

        phasor_type = ph_unit & 0xff000000
        scale = ph_unit & 0x00ffffff

        if phasor_type > 0:  # Current PH unit
            return scale, "i"
        else:
            return scale, "v"


    def set_analog_units(self, an_units):
        """
        ### set_analog_units() ###

        Setter for analog channels conversion factor.

        **Params:**

        * ``an_units`` **(list)** - Should be list of tuples ``(scale, analog_type)``
        where analog type is ``'pow'`` for single point-on-wave, ``'rms'`` for RMS of
        analog input and ``'peak`` for peak of analog input.
        If ``multistreaming`` should be list of lists.

        **Raises:**

            FrameError
        When ``an_units`` is not list of lists with length ``num_pmu`` when ``multistreaming``.
        When ``an_units`` element is not tuple.

        """

        if self._multistreaming:
            if not all(isinstance(el, list) for el in an_units) or self._num_pmu != len(an_units):
                raise FrameError("When NUM_PMU > 1 provide ANUNIT as list of lists.")

            anunit_list = []
            for i, an_unit in enumerate(an_units):
                if not all(isinstance(el, tuple) for el in an_unit) or self._analog_num[i] != len(an_unit):
                    raise FrameError("Provide ANUNIT as list of tuples with ANNMR elements. "
                                     "Ex: [(1234,'pow'),(1234, 'rms')]")

                an_values = []
                for an_tuple in an_unit:
                    an_values.append(ConfigFrame1._anunit2int(*an_tuple))

                anunit_list.append(an_values)

            self._an_units = anunit_list
        else:
            if not all(isinstance(el, tuple) for el in an_units) or self._analog_num != len(an_units):
                raise FrameError("Provide ANUNIT as list of tuples with ANNMR elements. "
                                 "Ex: [(1234,'pow'),(1234, 'rms')]")

            self._an_units = [ConfigFrame1._anunit2int(*anun) for anun in an_units]


    def get_analog_units(self):

        if all(isinstance(el, list) for el in self._an_units):
            return [[self._int2anunit(unit) for unit in an_unit] for an_unit in self._an_units]
        else:
            return [self._int2anunit(an_unit) for an_unit in self._an_units]


    @staticmethod
    def _anunit2int(scale, anunit_type="pow"):
        """
        ### anunit2int() ###

        Convert method for analog channels conversion factor.

        MSB: If analog type is ``pow`` then MSB will be ``0``.
        If analog type is ``rms`` then MSB will be ``1`` and
        if analog type is ``peak`` then MSB will be ``2``.

        LSB: Signed 24 bit word for user defined scaling.

        **Params:**

        * ``scale`` **(int)** - scale factor.
        * ``anunit_type`` **(char)** - ``pow`` - single point on wave,
        ``rms`` - RMS of analog input and ``peak`` - peak of analog input.
        Also might be user defined. Default value: ``pow``.

        **Returns:**

        * ``int`` which represents analog channels conversion factor.

        **Raises:**

            FrameError
        When ``scale`` is out of range.

        """

        if not -8388608 <= scale <= 8388608:
            raise FrameError("ANUNIT scale out of range. -8388608 <= ANUNIT <=  8388608.")

        scale &= 0xffffff  # 24-bit signed integer

        anunit = 1 << 24

        if anunit_type == "pow":  # TODO: User defined analog units
            anunit |= scale
            return anunit ^ (1 << 24)

        if anunit_type == "rms":
            anunit |= scale
            return anunit

        if anunit_type == "peak":
            anunit |= scale
            return anunit ^ (3 << 24)


    @staticmethod
    def _int2anunit(an_unit):

        TYPES = { "0": "pow", "1": "rms", "2": "peak" }

        an_unit_byte = an_unit.to_bytes(4, byteorder="big", signed=True)
        an_type = int.from_bytes(an_unit_byte[0:1], byteorder="big", signed=False)
        an_scale = int.from_bytes(an_unit_byte[1:4], byteorder="big", signed=True)

        return an_scale, TYPES[str(an_type)]


    def set_digital_units(self, dig_units):
        """
        ### set_digital_units() ###

        Setter for mask words for digital status words.

        Two 16 bit words are provided for each digital word.
        The first will be used to indicate the normal status of the
        digital inputs by returning 0 when XORed with the status word.

        The second will indicate the current valid inputs to the PMU
        by having a bit set in the binary position corresponding to the
         digital input and all other bits set to 0.

        **Params:**

        * ``dig_units`` **(list)** - Should be list of tuples ``(first_mask, second_mask)``.
        If ``multistreaming`` should be list of lists.

        **Raises:**

            FrameError
        When ``dig_units`` is not list of lists with length ``num_pmu`` when ``multistreaming``.
        When ``dig_units`` element is not tuple.

        """

        if self._multistreaming:
            if not all(isinstance(el, list) for el in dig_units) or self._num_pmu != len(dig_units):
                raise FrameError("When NUM_PMU > 1 provide DIGUNIT as list of lists.")

            digunit_list = []
            for i, dig_unit in enumerate(dig_units):
                if not all(isinstance(el, tuple) for el in dig_unit) or self._digital_num[i] != len(dig_unit):
                    raise FrameError("Provide DIGUNIT as list of tuples with DGNMR elements. "
                                     "Ex: [(0x0000,0xffff),(0x0011, 0xff0f)]")

                dig_values = []
                for dig_tuple in dig_unit:
                    dig_values.append(ConfigFrame1._digunit2int(*dig_tuple))

                digunit_list.append(dig_values)

            self._dig_units = digunit_list
        else:
            if not all(isinstance(el, tuple) for el in dig_units) or self._digital_num != len(dig_units):
                raise FrameError("Provide DIGUNIT as list of tuples with DGNMR elements. "
                                 "Ex: [(0x0000,0xffff),(0x0011, 0xff0f)]")

            self._dig_units = [ConfigFrame1._digunit2int(*dgun) for dgun in dig_units]


    def get_digital_units(self):

        if all(isinstance(el, list) for el in self._dig_units):
            return [[self._int2digunit(unit) for unit in dig_unit] for dig_unit in self._dig_units]
        else:
            return [self._int2digunit(dig_unit) for dig_unit in self._dig_units]


    @staticmethod
    def _digunit2int(first_mask, second_mask):
        """
        ### digunit2int() ###

        Generate digital status word mask.

        **Params:**

        * ``first_mask`` **(int)** - status indicator.
        * ``second_mask`` **(int)** - valid input indicator.

        **Returns:**

        * ``int`` which digital status word mask.

        **Raises:**

            FrameError
        When ``first_mask`` is out of range.
        When ``second_mask`` is out of range.

        """

        if not 0 <= first_mask <= 65535:
            raise FrameError("DIGUNIT first mask must be 16-bit word. 0x0000 <= first_mask <= 0xffff")

        if not 0 <= first_mask <= 65535:
            raise FrameError("DIGUNIT second mask must be 16-bit word. 0x0000 <= second_mask <= 0xffff")

        return (first_mask << 16) | second_mask

    @staticmethod
    def _int2digunit(dig_unit):

        first = dig_unit & 0xffff0000
        second = dig_unit & 0x0000ffff

        return first, second

    def set_fnom(self, f_nom):
        """
        ### set_fnom() ###

        Setter for nominal line frequency.

        Should be ``50`` or ``60`` Hz.

        **Params:**

        * ``f_nom`` **(int)** - ``50`` or ``60`` Hz. If ``multistreaming``
        should be list of ints.

        **Raises:**

            FrameError
        When ``f_nom`` is not ``50`` or ``60``.
        When ``f_nom`` is not list of int with length ``num_pmu`` when
        ``multistreaming``.

        """

        if self._multistreaming:
            if not isinstance(f_nom, list) or self._num_pmu != len(f_nom):
                raise FrameError("When NUM_PMU > 1 provide FNOM as list with NUM_PMU elements.")

            fnom_list = []
            for fnom in f_nom:
                fnom_list.append(ConfigFrame1._fnom2int(fnom))

            self._f_nom = fnom_list

        else:
            self._f_nom = ConfigFrame1._fnom2int(f_nom)


    def get_fnom(self):

        if isinstance(self._f_nom, list):
            return [self._int2fnom(fnom) for fnom in self._f_nom]
        else:
            return self._int2fnom(self._f_nom)


    @staticmethod
    def _fnom2int(fnom=60):
        """
        ### fnom2int() ###

        Convert line frequency to code.

        60 Hz = ``0`` and 50 Hz = ``1``.

        **Params:**

        * ``fnom`` **(int)** - Nominal line frequency. Default value: 60.

        **Returns:**

        * ``int`` [``0`` or ``1``]

        **Raises:**

            FrameError
        When ``fnom`` is not 50 or 60.

        """

        if fnom != 50 and fnom != 60:
            raise FrameError("Fundamental frequency must be 50 or 60.")

        if fnom == 50:
            return 1
        else:
            return 0


    @staticmethod
    def _init2fnom(fnom):

        if fnom:
            return 50
        else:
            return 60


    @staticmethod
    def _int2fnom(fnom_int):

        if fnom_int == 0:
            return 60
        else:
            return 50


    def set_cfg_count(self, cfg_count):
        """
        ### set_cfg_count() ###

        Setter for configuration change count.

        Factory default: ``0``. This count will be the number of changes
        of configuration of this message stream.

        **Params:**

        * ``cfg_count`` **(mixed)** - Number of changes. Sholud be list of ints
        if ``multistreaming``.

        **Raises:**

            FrameError.
        When ``cfg_count`` is not list of ints with length ``num_pmu`` when
        ``multistreaming``.
        When ``cfg_count`` is out of range.

        """

        if self._multistreaming:
            if not isinstance(cfg_count, list) or self._num_pmu != len(cfg_count):
                raise FrameError("When NUM_PMU > 1 provide CFGCNT as list with NUM_PMU elements.")

            cfgcnt_list = []
            for cfgcnt in cfg_count:
                if not 0 <= cfgcnt <= 65535:
                    raise FrameError("CFGCNT out of range. 0 <= CFGCNT <= 65535.")
                cfgcnt_list.append(cfgcnt)

            self._cfg_count = cfgcnt_list
        else:
            if not 0 <= cfg_count <= 65535:
                raise FrameError("CFGCNT out of range. 0 <= CFGCNT <= 65535.")
            self._cfg_count = cfg_count


    def get_cfg_count(self):

        return self._cfg_count


    def set_data_rate(self, data_rate):
        """
        ### set_data_rate() ###

        Setter for rate of phasor data transmission.

        If ``data_rate > 0`` rate is number of frames per second.
        If ``data_rate < 0`` rate is negative of seconds per frame.

        **Params:**

        * ``data_rate`` **(int)** - Rate of phasor data transmission.

        **Raises:**

            FrameError.
        When ``data_rate`` is out of range.

        """
        if not -32767 <= data_rate <= 32767:
            raise FrameError("DATA_RATE out of range. -32 767 <= DATA_RATE <= 32 767.")

        self._data_rate = data_rate


    def get_data_rate(self):

        return self._data_rate


    def convert2bytes(self):

        if not self._multistreaming:

            cfg_b = self._time_base.to_bytes(4, "big") + self._num_pmu.to_bytes(2, "big") + \
                    str.encode(self._station_name) + self._id_code.to_bytes(2, "big") + \
                    self._data_format.to_bytes(2, "big") + self._phasor_num.to_bytes(2, "big") + \
                    self._analog_num.to_bytes(2, "big") + self._digital_num.to_bytes(2, "big") + \
                    str.encode("".join(self._channel_names)) + list2bytes(self._ph_units, 4) + \
                    list2bytes(self._an_units, 4) + list2bytes(self._dig_units, 4) + \
                    self._f_nom.to_bytes(2, "big") + self._cfg_count.to_bytes(2, "big") + \
                    self._data_rate.to_bytes(2, "big", signed=True)
        else:

            cfg_b = self._time_base.to_bytes(4, "big") + self._num_pmu.to_bytes(2, "big")

            # Concatenate configurations as many as num_pmu tells
            for i in range(self._num_pmu):
                cfg_b_i = str.encode(self._station_name[i]) + self._id_code[i].to_bytes(2, "big") + \
                          self._data_format[i].to_bytes(2, "big") + self._phasor_num[i].to_bytes(2, "big") + \
                          self._analog_num[i].to_bytes(2, "big") + self._digital_num[i].to_bytes(2, "big") + \
                          str.encode("".join(self._channel_names[i])) + list2bytes(self._ph_units[i], 4) + \
                          list2bytes(self._an_units[i], 4) + list2bytes(self._dig_units[i], 4) + \
                          self._f_nom[i].to_bytes(2, "big") + self._cfg_count[i].to_bytes(2, "big")

                cfg_b += cfg_b_i

            cfg_b += self._data_rate.to_bytes(2, "big", signed=True)

        return super().convert2bytes(cfg_b)


    @staticmethod
    def convert2frame(byte_data):

        try:

            if not CommonFrame._check_crc(byte_data):
                raise FrameError("CRC failed. Configuration frame not valid.")

            pmu_code = int.from_bytes(byte_data[4:6], byteorder="big", signed=False)
            soc = int.from_bytes(byte_data[6:10], byteorder="big", signed=False)
            frasec = CommonFrame._int2frasec(int.from_bytes(byte_data[10:14], byteorder="big", signed=False))

            time_base_int = int.from_bytes(byte_data[14:18], byteorder="big", signed=False)
            time_base = time_base_int & 0x00ffffff  # take only first 24 LSB bits

            num_pmu = int.from_bytes(byte_data[18:20], byteorder="big", signed=False)

            start_byte = 20

            if num_pmu > 1:  # Loop through configurations for each

                station_name, id_code, data_format, phasor_num, analog_num, digital_num, channel_names, ph_units, \
                an_units, dig_units, fnom, cfg_count = [[] for _ in range(12)]

                for i in range(num_pmu):

                    station_name.append(byte_data[start_byte:start_byte+16].decode("ascii"))
                    start_byte += 16

                    id_code.append(int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False))
                    start_byte += 2

                    data_format.append(int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                                       & 0x000f)
                    start_byte += 2

                    phasor_num.append(int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False))
                    start_byte += 2

                    analog_num.append(int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False))
                    start_byte += 2

                    digital_num.append(int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False))
                    start_byte += 2

                    stream_channel_names = []
                    for _ in range(phasor_num[i] + analog_num[i] + 16*digital_num[i]):
                        stream_channel_names.append(byte_data[start_byte:start_byte+16].decode("ascii"))
                        start_byte += 16

                    channel_names.append(stream_channel_names)

                    stream_ph_units = []
                    for _ in range(phasor_num[i]):
                        ph_unit = int.from_bytes(byte_data[start_byte:start_byte+4], byteorder="big", signed=False)
                        stream_ph_units.append(ConfigFrame1._int2phunit(ph_unit))
                        start_byte += 4

                    ph_units.append(stream_ph_units)

                    stream_an_units = []
                    for _ in range(analog_num[i]):
                        an_unit = int.from_bytes(byte_data[start_byte:start_byte+4], byteorder="big", signed=True)
                        stream_an_units.append(ConfigFrame1._int2anunit(an_unit))
                        start_byte += 4

                    an_units.append(stream_an_units)

                    stream_dig_units = []
                    for _ in range(digital_num[i]):
                        stream_dig_units.append(ConfigFrame1._int2digunit(
                                int.from_bytes(byte_data[start_byte:start_byte+4], byteorder="big", signed=False)))
                        start_byte += 4

                    dig_units.append(stream_dig_units)

                    fnom.append(ConfigFrame1._int2fnom(int.from_bytes(byte_data[start_byte:start_byte + 2],
                                                                      byteorder="big", signed=False)))
                    start_byte += 2

                    cfg_count.append(int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False))
                    start_byte += 2

            else:

                station_name = byte_data[start_byte:start_byte+16].decode("ascii")
                start_byte += 16

                id_code = int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                start_byte += 2

                data_format_int = int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                data_format = data_format_int & 0x000f  # Take only first 4 LSB bits
                start_byte += 2

                phasor_num = int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                start_byte += 2

                analog_num = int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                start_byte += 2

                digital_num = int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                start_byte += 2

                channel_names = []
                for _ in range(phasor_num + analog_num + 16*digital_num):
                    channel_names.append(byte_data[start_byte:start_byte+16].decode("ascii"))
                    start_byte += 16

                ph_units = []
                for _ in range(phasor_num):
                    ph_unit_int = int.from_bytes(byte_data[start_byte:start_byte+4], byteorder="big", signed=False)
                    ph_units.append(ConfigFrame1._int2phunit(ph_unit_int))
                    start_byte += 4

                an_units = []
                for _ in range(analog_num):
                    an_unit = int.from_bytes(byte_data[start_byte:start_byte+4], byteorder="big", signed=False)
                    an_units.append(ConfigFrame1._int2anunit(an_unit))
                    start_byte += 4

                dig_units = []
                for _ in range(digital_num):
                    dig_units.append(ConfigFrame1._int2digunit(
                                int.from_bytes(byte_data[start_byte:start_byte+4], byteorder="big", signed=False)))
                    start_byte += 4

                fnom = ConfigFrame1._int2fnom(int.from_bytes(byte_data[start_byte:start_byte + 2],
                                                             byteorder="big", signed=False))
                start_byte += 2

                cfg_count = int.from_bytes(byte_data[start_byte:start_byte+2], byteorder="big", signed=False)
                start_byte += 2

            data_rate = int.from_bytes(byte_data[-4:-2], byteorder="big", signed=True)

            return ConfigFrame1(pmu_code, time_base, num_pmu, station_name, id_code, data_format, phasor_num,
                                analog_num, digital_num, channel_names, ph_units, an_units, dig_units, fnom, cfg_count,
                                data_rate, soc, frasec)

        except Exception as error:
            raise FrameError("Error while creating Config frame: " + str(error))

class FrameError(BaseException):
    pass
