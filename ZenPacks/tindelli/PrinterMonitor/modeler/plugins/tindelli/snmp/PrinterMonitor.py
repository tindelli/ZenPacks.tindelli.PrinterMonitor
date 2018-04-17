from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap

class PrinterMonitor(SnmpPlugin):

    # Basic SNMP attribute maps
    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.43.5.1.1.17.1': 'prtGeneralSerialNumber',
#        '.1.3.6.1.2.1.43.10.2.1.2.1.1': 'prtMarkerMarkTech',
        '.1.3.6.1.2.1.43.10.2.1.6.1.1': 'numberColors',
    })

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        maps = []

        maps.append(ObjectMap(
            compname = 'hw',
            data={
                'serialnumber': getData['prtGeneralSerialNumber'],
            }
        ))

        maps.append(ObjectMap(
            data={
                'colorSupport': True if getData['numberColors'] else False,
                'prtMarkerMarkTech': PrtMarkerMarkTechTC[getdata['prtMarkerMarkTech']]
            }
        ))

        return maps
