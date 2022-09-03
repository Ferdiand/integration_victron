## Introduction
Victron products which feature the VE.Direct serial communications interface allow simple access to
detailed information of that product. This document describes how to receive and interpret this
information.

See our Data communication whitepaper for more information on other protocols and products
available: [Whitepaper-Data-communication-with-Victron-Energy-products_EN.pdf](http://www.victronenergy.com/upload/documents/Whitepaper-Data-communication-with-Victron-Energy-products_EN.pdf)

The VE.Direct interface includes two modes: Text-mode and the HEX-mode. The purpose of the
Text-mode is to make retrieving information extremely simple. The product will periodically
transmit all run-time fields. The HEX-mode allows not only to read data but also write data, for
example, change settings.

There are two different implementations of the Text-mode and HEX-mode:

__Older implementations:__

- On power up, a VE.Direct interface will always be in Text-mode, and continuously transmits
all run-time fields. As soon as it receives a valid HEX-message, it will switch to HEX-mode. It
will stay in HEX-mode as long as HEX-messages are frequently received. After a product has
not received any valid HEX-messages for several seconds, it will switch back to Text-mode
and start to auto transmit the run-time fields periodically again. Some products will send
Asynchronous HEX-messages, starting with “:A” and ending with a newline ‘\n’, on their
own. These messages can interrupt a regular Text-mode frame.

__Newer implementations__
- Always have the Text-mode active, regardless of the HEX-messages.

To know more which implementation is applied to your product, please check its specific VE.Direct protocol document.

This document only describes the Text-mode.

Make sure to also read our [VE.Direct protocol FAQ](http://www.victronenergy.com/live/vedirect_protocol:faq), and the [Open source page on Victron Live](http://www.victronenergy.com/live/open_source:start) which lists projects from other people using our VE.Direct protocol

## Physical interface

The VE.Direct interface is accessed via a 4-pin connector. The picture below shows where the VE.Direct connector is located on a BMV-700.



Pin Producer Consumer
1 GND GND
2 VE.Direct-RX VE.Direct-RX
3 VE.Direct-TX VE.Direct-TX
4 Power + Power +


Producers are products, such as the BMV battery monitor and the MPPT solar chargers. Consumers are products reading the data, such as the Color Control GX. When connecting a Producer to a Consumer, the Producer’s VE.Direct-TX must be connected to Consumer VE.Direct-RX. The same goes to the Producer VE.Direct-RX, which must be connected to Consumer’s VE.Direct-TX. Note that the pins on the MPPT can have alternative functions. Its VE.Direct-RX pin can be used to switch the charger on and off. Its VE.Direct-TX pin can be configured to send a PWM signal, to dim (street)lights. For details about the connector type see the information at the end of this document.

A VE.Direct to USB interface cable can be purchased from Victron Energy (“VE.Direct to USB”, part number ASS030530000). This interface cable provides a virtual comport through USB as well as galvanic isolation.

A VE.Direct to RS232 interface cable can also be purchased from Victron Energy (“VE.Direct to RS232 interface”, part number ASS030520500)

## Serial port configuration

- Baud rate: 19200
- Data bits: 8
- Parity: None
- Stop bits: 1
- Flow control: None

## Pins to use when using the VE.Direct to RS232 interface

For the communication use the GND, RX and TX pins: pin 5, 2 and 3 on the DB9 connector.

Also the DTR signal (pin 4 on the DB9 connector) and/or the RTS signal (pin 7 on the DB9 connector) must be driven high to power the isolated side of the interface. How to program the DTR and RTS differs between used operating systems and hardware.

For more details see:
[https://www.victronenergy.com/live/vedirect_protocol:faq#q2when_using_the_vedirect_to_rs232_interface_what_pins_do_i_need](https://www.victronenergy.com/live/vedirect_protocol:faq#q2when_using_the_vedirect_to_rs232_interface_what_pins_do_i_need)

## Message format
The device transmits blocks of data at 1 second intervals. Each field is sent using the following format:

`<Newline><Field-Label><Tab><Field-Value>`


The identifiers are defined as follows:
- `<Newline>`: A carriage return followed by a line feed (0x0D, 0x0A).
- `<Field-Label>`: An arbitrary length label that identifies the field. Where applicable, this will be the same as the label that is used on the LCD.
- `<Tab>`: A horizontal tab (0x09).
- `<Field-Value>`: The ASCII formatted value of this field. The number of characters transmitted depends on the magnitude and sign of the value

## Data integrity
The statistics are grouped in blocks with a checksum appended. The last field in a block will always be “Checksum”. The value is a single byte, and will not necessarily be a printable ASCII character. The modulo 256 sum of all bytes in a block will equal 0 if there were no transmission errors. Multiple blocks are sent containing different fields.

For more details see:
[https://www.victronenergy.com/live/vedirect_protocol:faq#q8how_do_i_calculate_the_text_checksum](https://www.victronenergy.com/live/vedirect_protocol:faq#q8how_do_i_calculate_the_text_checksum)

## Fields
The values sent over the serial communications interface do not necessarily use the same units as the values on the LCD.

### __V__ [mV] : Main or channel 1 (battery) voltage
### __VPV__ [mV] Panel voltage
### __PPV__ [W] Panel power
### __I__ [mA] Main or channel 1 battery current
### __IL__ [mA] Load current
### _LOAD_ Load output state (ON/OFF)
### _Relay_ Relay state
### _AR_ Alarm reason

### _OR_ Off reason

### _H19_ [0.01 kWh] Yield total (user resettable counter)
### _H20_ [0.01 kWh] Yield today
### __H21__ [W] Maximum power today
### _H22_ [0.01 kWh] Yield yesterday
### __H23__ [W] Maximum power yesterday
### _ERR_ Error code

### _CS_ State of operation
0. Off
2. Fault 2
3. Bulk
4. Absorption
5. Float
6. Storage
7. Equalize (manual)
9. Inverting
11. Power supply
245. Starting-up
246. Repeated absorption
247. Auto equalize / Recondition
248. BatterySafe
252. External Control

### __FW__ Firmware version (16 bit)

### __PID__ Product ID

### __SER#__ Serial number
### _HSDS_ Day sequence number (0..364)
### _MPPT_ Tracker operation mode

