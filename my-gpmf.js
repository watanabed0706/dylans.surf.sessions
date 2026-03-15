const gpmfExtract = require('gpmf-extract');
const goproTelemetry = require(`gopro-telemetry`);
const fs = require('fs');

const file = fs.readFileSync(process.argv[2]);

gpmfExtract(file)
  .then(extracted => {
    goproTelemetry(extracted, {}, telemetry => {
      fs.writeFileSync('data/gpmf.json', JSON.stringify(telemetry));
      //console.log('Telemetry saved as JSON');
    });
  })
  .catch(error => console.error(error));
