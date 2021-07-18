# esp32-sensor-reader

This is a version of my [Pi Sensor Reader](https://github.com/VirtualWolf/pi-sensor-reader) for reading temperature and humidity values from an attached DHT22/AM2302 sensor and posting them to an HTTP endpoint, but written in Python for use with [MicroPython on an ESP32 microcontroller](https://micropython.org).

Updates that fail to be sent — if the server is down, or you have no internet connection, etc. — will be written to the `queue` directory and attempted to be re-posted every five minutes.

## Helpful tools
* [micropy-cli](https://github.com/BradenM/micropy-cli)
* [Pymakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr)

## Setup
It requires a file called `config.json` at the root of the `src` directory, configured with your wifi network name and password, the GPIO pin that the DHT22 sensor is connected to, endpoint to periodically post data to, and the API key that protects that endpoint. An example file is given in [example.json](src/example.json).

## Endpoints
esp32-sensor-reader has four HTTP endpoints:
* `GET /` — Get the current temperature and humidity values.
* `GET /log` — View the log file that's written to when errors occur.
* `DELETE /log` — Clear the log file; this requires the `X-API-Key` header to be set with the same value as what you're sending to the endpoint.
* `POST /reset` — Restarts the ESP32; as above, it requires the `X-API-Key` header to be set.

## Options
* `local_only` — If set to `true`, the ESP32 won't attempt to post sensor updates anywhere and will just run the local webserver for polling
