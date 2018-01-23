var BME280 = require('node-adafruit-bme280')
 
BME280.probe(function(temperature, pressure, humidity) {
  console.log(temperature);
  console.log(pressure);
  console.log(humidity);
});
