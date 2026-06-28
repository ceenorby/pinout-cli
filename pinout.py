#!/usr/bin/env python3
import sys

# High-contrast color escape codes
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# The Comprehensive Component Database
CHIP_DATABASE = {
    # --- OP-AMPS & TIMERS ---
    "lm741": {
        "name": "LM741 Operational Amplifier (PDIP-8)",
        "description": "Classic single operational amplifier used for analog signal conditioning and filtering.",
        "ascii_art": f"""
               {BOLD}LM741 Top View{RESET}
            +---\\_/---+
      OFFSET| 1     8 | NC (No Connect)
     - INPUT| 2     7 | V+ (Positive Supply, Max +18V)
     + INPUT| 3     6 | OUTPUT
          V-| 4     5 | OFFSET
            +---------+
        """
    },
    "lm358": {
        "name": "LM358 Dual Operational Amplifier (PDIP-8)",
        "description": "Low-power dual op-amp. Highly useful because it contains two independent op-amps in a single 8-pin package.",
        "ascii_art": f"""
               {BOLD}LM358 Top View{RESET}
             +---\\_/---+
     OUT A   | 1     8 | VCC (Single/Dual Supply, 3V to 32V)
     -INPUT A| 2     7 | OUT B
     +INPUT A| 3     6 | -INPUT B
     GND/V-  | 4     5 | +INPUT B
             +---------+
        """
    },
    "ne555": {
        "name": "NE555 Precision Timer IC (PDIP-8)",
        "description": "Highly versatile timer IC used for creating precise clock pulses, delays, and PWM oscillation.",
        "ascii_art": f"""
               {BOLD}NE555 Top View{RESET}
            +---\\_/---+
         GND| 1     8 | VCC (4.5V to 16V)
     TRIGGER| 2     7 | DISCHARGE
      OUTPUT| 3     6 | THRESHOLD
       RESET| 4     5 | CONTROL VOLTAGE
            +---------+
        """
    },

    # --- MOTOR DRIVERS & REGISTERS ---
    "l293d": {
        "name": "L293D Dual H-Bridge Motor Driver (PDIP-16)",
        "description": "High-current driver designed to control bidirectional speed and direction of up to two DC motors.",
        "ascii_art": f"""
               {BOLD}L293D Top View{RESET}
            +---\\_/---+
     1,2EN  | 1    16 | VCC1 (Logic Supply, 5V)
     1A     | 2    15 | 4A
     1Y     | 3    14 | 4Y
     GND    | 4    13 | GND
     GND    | 5    12 | GND
     2Y     | 6    11 | 3Y
     2A     | 7    10 | 3A
     VCC2   | 8     9 | 3,4EN (Motor Power, 4.5V to 36V)
            +---------+
        """
    },
    "74hc595": {
        "name": "74HC595 8-Bit Shift Register (PDIP-16)",
        "description": "Serial-In Parallel-Out shift register. Used to expand limited GPIO pins to control 8 outputs with just 3 MCU pins.",
        "ascii_art": f"""
               {BOLD}74HC595 Top View{RESET}
         QB  | 1    16 | VCC (2V to 6V)
         QC  | 2    15 | QA (First Output Bit)
         QD  | 3    14 | SER (Serial Data Input)
         QE  | 4    13 | OE (Output Enable, Active Low)
         QF  | 5    12 | RCLK (Storage Latch/Register Clock)
         QG  | 6    11 | SRCLK (Shift Register Clock)
         QH  | 7    10 | SRCLR (Shift Register Clear, Active Low)
        GND  | 8     9 | QH' (Serial Out, Daisy Chain Link)
             +---------+
        """
    },

    # --- LOGIC GATES & COUNTERS ---
    "74hc00": {
        "name": "74HC00 Quad 2-Input NAND Gate (PDIP-14)",
        "description": "Four independent NAND gates. A fundamental building block of digital logic systems.",
        "ascii_art": f"""
               {BOLD}74HC00 Top View{RESET}
             +---\\_/---+
         1A  | 1    14 | VCC (2V to 6V)
         1B  | 2    13 | 4B
         1Y  | 3    12 | 4A
         2A  | 4    11 | 4Y
         2B  | 5    10 | 3B
         2Y  | 6     9 | 3A
         GND | 7     8 | 3Y
             +---------+
        """
    },
    "74hc14": {
        "name": "74HC14 Hex Inverter with Schmitt Trigger (PDIP-14)",
        "description": "Six independent NOT gates with hysteresis, perfect for debouncing switches and squaring up noisy signals.",
        "ascii_art": f"""
               {BOLD}74HC14 Top View{RESET}
             +---\\_/---+
         1A  | 1    14 | VCC (2V to 6V)
         1Y  | 2    13 | 6A
         2A  | 3    12 | 6Y
         2Y  | 4    11 | 5A
         3A  | 5    10 | 5Y
         3Y  | 6     9 | 4A
         GND | 7     8 | 4Y
             +---------+
        """
    },
    "cd4017": {
        "name": "CD4017 CMOS Decade Counter (PDIP-16)",
        "description": "5-stage Johnson decade counter that produces sequential outputs from 0 to 9 on incoming clock pulses.",
        "ascii_art": f"""
               {BOLD}CD4017 Top View{RESET}
             +---\\_/---+
         Q5  | 1    16 | VDD (3V to 15V)
         Q1  | 2    15 | RESET (Active High)
         Q0  | 3    14 | CLOCK (Clock Input)
         Q2  | 4    13 | CLOCK INHIBIT (Active High)
         Q7  | 5    12 | CARRY OUT (Div-by-10)
         Q3  | 6    11 | Q9
         Q8  | 7    10 | Q4
         GND | 8     9 | Q6
             +---------+
        """
    },

    # --- DISCRETE TRANSISTORS ---
    "bc547": {
        "name": "BC547 NPN Bipolar Junction Transistor (TO-92)",
        "description": "General purpose small-signal NPN transistor. Highly used for switching and amplification in labs.",
        "ascii_art": f"""
               {BOLD}BC547 TO-92 Front View{RESET}
                  (Flat Face)
                  .---------.
                 /   {BOLD}BC547{RESET}   \\
                |  {BOLD}C{RESET}   {BOLD}B{RESET}   {BOLD}E{RESET}  |
                |  |   |   |  |
                |  |   |   |  |
                   1   2   3
                   
                Pin 1: {CYAN}Collector{RESET}
                Pin 2: {CYAN}Base{RESET}
                Pin 3: {CYAN}Emitter{RESET}
        """
    },
    "irf540n": {
        "name": "IRF540N N-Channel Power MOSFET (TO-220)",
        "description": "High-current N-Channel Power MOSFET (100V, 33A). Used for switching high power loads from logic pins.",
        "ascii_art": f"""
               {BOLD}IRF540N TO-220 Front View{RESET}
                  +------------+
                  |  [ Metal ] |
                  |  [ Tab   ] |
                  |------------|
                  |  {BOLD}IRF540N{RESET}   |
                  |  {BOLD}G{RESET}   {BOLD}D{RESET}   {BOLD}S{RESET}   |
                  |  |   |   |   |
                     1   2   3
                     
                Pin 1: {CYAN}Gate{RESET} (Trigger)
                Pin 2: {CYAN}Drain{RESET} (Connected to Load V-)
                Pin 3: {CYAN}Source{RESET} (Connected to System GND)
        """
    },

    # --- MICROCONTROLLERS & MICROPROCESSORS ---
    "atmega328p": {
        "name": "ATmega328P Microcontroller (28-pin PDIP)",
        "description": "High-performance, low-power AVR 8-bit RISC microcontroller used on the Arduino Uno.",
        "ascii_art": f"""
                                {BOLD}ATmega328P (Top View){RESET}
                                    +-------\\_/-------+
                (PCINT14/RESET) PC6 | 1             28 | PC5 (ADC5/SCL/PCINT13)
                  (PCINT16/RXD) PD0 | 2             27 | PC4 (ADC4/SDA/PCINT12)
                  (PCINT17/TXD) PD1 | 3             26 | PC3 (ADC3/PCINT11)
                 (PCINT18/INT0) PD2 | 4             25 | PC2 (ADC2/PCINT10)
                 (PCINT19/INT1) PD3 | 5             24 | PC1 (ADC1/PCINT9)
               (PCINT20/XCK/T0) PD4 | 6             23 | PC0 (ADC0/PCINT8)
                                VCC | 7             22 | GND
                                GND | 8             21 | AREF
           (PCINT6/XTAL1/TOSC1) PB6 | 9             20 | AVCC (ADC Power Supply Input)
           (PCINT7/XTAL2/TOSC2) PB7 | 10            19 | PB5 (SCK/PCINT5)
              (PCINT21/OC0B/T1) PD5 | 11            18 | PB4 (MISO/PCINT4)
            (PCINT22/OC0A/AIN0) PD6 | 12            17 | PB3 (MOSI/OC2A/PCINT3)
                 (PCINT23/AIN1) PD7 | 13            16 | PB2 (SS/OC1B/PCINT2)
             (PCINT0/CLKO/ICP1) PB0 | 14            15 | PB1 (OC1A/PCINT1)
                                    +------------------+
        """
    },
    "esp32-s3": {
        "name": "ESP32-S3 Raw IC (QFN56 Layout Variant)",
        "description": "Dual-core Xtensa 32-bit LX7 MCU with built-in Wi-Fi and Bluetooth LE. Excellent for IoT and AI-enabled edge hardware.",
        "ascii_art": f"""
                        {BOLD}ESP32-S3 (Top View Pin-Map Guide){RESET}
                      +-------------------------------+
                      | 56 55 54 53 52 51 50 49 48 47 |
              GND  1  | [ ] [ ] [ ] [ ] [ ] [ ] [ ]   | 46  IO9
              3V3  2  |                               | 45  IO10
             RSTN  3  |                               | 44  IO11
              IO1  4  |                               | 43  IO12
              IO2  5  |                               | 42  IO13
              IO3  6  |                               | 41  IO14
              IO4  7  |                               | 40  XTAL_P
              IO5  8  |                               | 39  XTAL_N
              IO6  9  |                               | 38  GND
              IO7 10  |                               | 37  IO17
              IO8 11  |                               | 36  IO18
                      |   [ ] [ ] [ ] [ ] [ ] [ ]     |
                      +-------------------------------+
                         12 13 14 15 16 17 18 19 20 21
                         
        {YELLOW}Note: Check exact hardware datasheet variant footprints before routing multi-layer PCBs!{RESET}
        """
    },
    "esp8266": {
        "name": "NodeMCU ESP8266 Dev Board (ESP-12E)",
        "description": "Massively popular, low-cost Wi-Fi enabled development board. Ideal for basic IoT prototyping.",
        "ascii_art": f"""
                             {BOLD}NodeMCU ESP8266 (Top View Pinout){RESET}
                            +-------------------------------+
                    [ USB ] | [ ] ADC0/A0       [ ] VIN (5V)|
                            | [ ] RSV           [ ] GND     |
                            | [ ] RSV           [ ] RST     |
                            | [ ] SD3/GPIO10    [ ] EN      |
                            | [ ] SD2/GPIO9     [ ] 3V3     |
                            | [ ] SD1/MOSI      [ ] GND     |
                            | [ ] CMD/CS        [ ] TXD0/D0 |
                            | [ ] SD0/MISO      [ ] RXD0/D1 |
                            | [ ] CLK/SCLK      [ ] GPIO15  |
                            | [ ] GND           [ ] GPIO13  |
                            | [ ] 3V3           [ ] GPIO12  |
                            | [ ] EN            [ ] GPIO14  |
                            | [ ] RST           [ ] GND     |
                            | [ ] GND           [ ] 3V3     |
                            | [ ] VIN           [ ] GPIO1   |
                            +-------------------------------+
        """
    },
    "pico": {
        "name": "Raspberry Pi Pico (RP2040 Chip Dual-Row Board)",
        "description": "Low-cost, high-performance microcontroller board built using the custom RP2040 silicon chip designed by Raspberry Pi.",
        "ascii_art": f"""
                           {BOLD}Raspberry Pi Pico (Top View){RESET}
                              +------------------------------+
               GP0 (UART0 TX) | 1                         40 | VBUS (USB Power, 5V Input)
               GP1 (UART0 RX) | 2                         39 | VSYS (System Power Input)
                          GND | 3                         38 | GND
               GP2            | 4                         37 | 3V3_EN (Regulator Enable)
               GP3            | 5                         36 | 3V3 (3.3V Output, Max 300mA)
               GP4 (I2C1 SDA) | 6                         35 | ADC_VREF
               GP5 (I2C1 SCL) | 7                         34 | GP28 (ADC2)
                          GND | 8                         33 | GND
               GP6            | 9                         32 | GP27 (ADC1)
               GP7            | 10                        31 | GP26 (ADC0)
               GP8            | 11                        30 | RUN (Reset, Active Low)
               GP9            | 12                        29 | GP22
                          GND | 13                        28 | GND
              GP10            | 14                        27 | GP21
              GP11            | 15                        26 | GP20
              GP12            | 16                        25 | GP19 (SPI0 MOSI)
              GP13            | 17                        24 | GP18 (SPI0 MISO)
                          GND | 18                        23 | GND
              GP14            | 19                        22 | GP17 (SPI0 CS)
              GP15            | 20                        21 | GP16 (SPI0 SCK)
                              +--[ DEBUG ]------------------+
        """
    },
    "stm32": {
        "name": "STM32F103C8T6 ARM Cortex-M3 Dev Board ('Blue Pill')",
        "description": "Affordable 32-bit ARM Cortex-M3 microcontroller board. Widely used for teaching professional embedded engineering systems.",
        "ascii_art": f"""
                            {BOLD}STM32 Blue Pill (Top View Pinout){RESET}
                           +---------------------------------+
                       B12 | [ ]                         [ ] | GND
                       B13 | [ ]                         [ ] | GND
                       B14 | [ ]                         [ ] | 3V3
                       B15 | [ ]                         [ ] | R (Reset)
                        A8 | [ ]                         [ ] | B11
                        A9 | [ ]  (TX1)                  [ ] | B10 (I2C2 SCL)
                       A10 | [ ]  (RX1)                  [ ] | B1  (ADC9)
                       A11 | [ ]  (USB D-)               [ ] | B0  (ADC8)
                       A12 | [ ]  (USB D+)               [ ] | A7  (SPI1 MOSI)
                       A15 | [ ]                         [ ] | A6  (SPI1 MISO)
                        B3 | [ ]                         [ ] | A5  (SPI1 SCK)
                        B4 | [ ]                         [ ] | A4  (SPI1 NSS)
                        B5 | [ ]                         [ ] | A3  (ADC3)
                        B6 | [ ]  (I2C1 SCL)             [ ] | A2  (ADC2 / TX2)
                        B7 | [ ]  (I2C1 SDA)             [ ] | A1  (ADC1 / RX2)
                        B8 | [ ]                         [ ] | A0  (ADC0 / Wakeup)
                        B9 | [ ]                         [ ] | C15 (OSC Out)
                        5V | [ ]                         [ ] | C14 (OSC In)
                       GND | [ ]                         [ ] | C13 (Built-in LED)
                       3V3 | [ ]                         [ ] | VBAT (RTC Backup Power)
                           +-------------[ USB ]-------------+
        """
    },

    # --- POPULAR LAB SENSORS ---
    "hc-sr04": {
        "name": "HC-SR04 Ultrasonic Distance Sensor Module",
        "description": "Non-contact ultrasonic range measurement module (2cm to 400cm range). Uses sonic pulses and echoes.",
        "ascii_art": f"""
               {BOLD}HC-SR04 Front & Connector View{RESET}
               +---------------------------------+
               |   [ Transmitter ]   [ Receiver ]|
               |       (T)               (R)     |
               +---------------===---------------+
                               |||
                               1234
                               
                   Pin 1: {RED}VCC{RESET} (+5V DC Input)
                   Pin 2: {CYAN}TRIG{RESET} (Trigger Input: 10us High pulse starts ping)
                   Pin 3: {CYAN}ECHO{RESET} (Echo Output: Duration of High signal = flight time)
                   Pin 4: {BOLD}GND{RESET} (System Ground)
        """
    },
    "dht11": {
        "name": "DHT11/DHT22 Temperature & Humidity Sensor",
        "description": "Digital humidity and temperature sensor. Highly used in smart building or agricultural lab setups.",
        "ascii_art": f"""
               {BOLD}DHT11 / DHT22 (Pins Facing You){RESET}
                     .---------------.
                    | [][][][][][][] |
                    | [][][][][][][] |
                    | [][][][][][][] |
                    |                |
                    '----------------'
                       |   |   |   |
                       1   2   3   4
                       
                   Pin 1: {RED}VCC{RESET} (3.3V to 5.5V Power)
                   Pin 2: {CYAN}DATA{RESET} (Single-bus bidirectional data link)
                   Pin 3: {BOLD}NC{RESET} (No Connect - Leave empty)
                   Pin 4: {BOLD}GND{RESET} (System Ground)
        """
    }
}

# Add alias triggers so users don't have to guess spelling configurations
CHIP_DATABASE["dht22"] = CHIP_DATABASE["dht11"]
CHIP_DATABASE["bluepill"] = CHIP_DATABASE["stm32"]
CHIP_DATABASE["nodemcu"] = CHIP_DATABASE["esp8266"]
CHIP_DATABASE["hcsr04"] = CHIP_DATABASE["hc-sr04"]

def search_chip(query):
    query = query.lower().strip().replace("-", "").replace(" ", "")
    
    # Try finding exact matches by processing the database keys without dashes
    matched_key = None
    for key in CHIP_DATABASE:
        processed_key = key.replace("-", "")
        if query == processed_key:
            matched_key = key
            break
            
    if matched_key:
        chip = CHIP_DATABASE[matched_key]
        print(f"\n{GREEN}{BOLD}=== {chip['name']} ==={RESET}")
        print(f"{CYAN}Info:{RESET} {chip['description']}")
        print(chip['ascii_art'])
    else:
        print(f"\n{YELLOW}[!] Chip '{query}' not found in local inventory database.{RESET}")
        print(f"{BOLD}💡 Available Components Include:{RESET}")
        
        # Pretty-print available keys to the student in 4 neat columns
        keys = sorted(list(CHIP_DATABASE.keys()))
        # Filter out aliases to prevent duplication in list
        keys = [k for k in keys if k not in ["dht22", "bluepill", "nodemcu", "hcsr04"]]
        
        for i in range(0, len(keys), 4):
            chunk = keys[i:i+4]
            print("  " + "".join(f"{k:<15}" for k in chunk))
        print("\nTo add a new component, open `pinout.py` and append it to `CHIP_DATABASE`!\n")

def main():
    if len(sys.argv) < 2:
        print(f"{BOLD}Usage:{RESET} pinout <chip-name>")
        print("Example: pinout lm358")
        sys.exit(1)
        
    query = sys.argv[1]
    search_chip(query)

if __name__ == "__main__":
    main()



