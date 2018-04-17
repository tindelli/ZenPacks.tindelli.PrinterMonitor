from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap

class PrinterMonitor(SnmpPlugin):

    ###########################################################################
    # Text Conversion definitions from RFC 3805
    ###########################################################################

    # The type of marking technology used for this marking subunit
    PrtMarkerMarkTechTC = {
        1: 'other',
        2:  'unknown',
        3:  'LED',                              # electrophotographicLED
        4:  'Laser',                            # electrophotographicLaser
        5:  'Other Electrophotographic',        # electrophotographicOther
        6:  '9-pin Dot Matrix',                 # impactMovingHeadDotMatrix9pin
        7:  '24-pin Dot Matrix',                # impactMovingHeadDotMatrix24pin
        8:  'Other Dot Matrix',                 # impactMovingHeadDotMatrixOther
        9:  'Impact Moving Head Fully Formed',  # impactMovingHeadFullyFormed
        10: 'Impact Band',                      # impactBand
        11: 'Impact Other',                     # impactOther
        12: 'Inkjet (Aqueous)',                 # inkjetAqueous
        13: 'Inkjet (Solid)',                   # inkjetSolid
        14: 'Inkjet (Other)',                   # inkjetOther  
        15: 'Pen',
        16: 'Thermal Transfer',                 
        17: 'Thermal Sensitive',
        18: 'Thermal Diffusion',
        19: 'Thermal Other',
        20: 'Electroerosion',
        21: 'Electrostatic',
        22: 'Photographic Microfiche',
        23: 'Photographic Imagesetter',
        24: 'Photographic Other',
        25: 'Ion Deposition',
        26: 'eBeam',
        27: 'Typesetter',
    }

    # Basic SNMP attribute maps
    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.43.5.1.1.17.1': 'prtGeneralSerialNumber',
        '.1.3.6.1.2.1.43.10.2.1.2.1.1': 'prtMarkerMarkTech',
        '.1.3.6.1.2.1.43.10.2.1.6.1.1': 'numberColors',
    })

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getData, tableData = results

        maps = []

        maps.append(ObjectMap(
            compname = 'hw',
            data={
                'serialnumber': getData['prtGeneralSerialNumber'],
            }
        ))

        maps.append(ObjectMap(
            data={
                'colorSupport': True if getdata['numberColors'] else False,
                'prtMarkerMarkTech': PrtMarkerMarkTechTC[getData['prtMarkerMarkTech']]
            }
        ))

        return maps
