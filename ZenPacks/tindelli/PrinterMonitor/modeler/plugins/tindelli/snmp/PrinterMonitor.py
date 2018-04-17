from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap

class PrinterMonitor(SnmpPlugin):
    # Uses Printer-MIB v2 at oid 1.3.6.1.2.1.43
    # 1.3.6.1.2.1.43 printmib
    # .5 prtGeneral
    #   .1 prtGeneralTable
    #     .1.16 prtGeneralPrinterName
    #     .1.17 prtGeneralSerialNumber
    # .6 prtCover
    # .7 prtLocalization
    # .8 prtInput
    # .9 prtOutput
    # .10 prtMarker
    #   .2 prtMarkerTable
    #     .1.2 prtMarkerMarkTech (PrtMarkerMarkTechTC)
    #     .1.6 prtMarkerProcessColorants  
    # { printmib 11 } prtMarkerSupplies
    # { printmib 12 } prtMarkerColorant
    # { printmib 13 } prtMediaPath
    # { printmib 14 } prtChannel
    # { printmib 15 } prtInterpreter
    # { printmib 16 } prtConsoleDisplayBuffer
    # { printmib 17 } prtConsoleLights
    # { printmib 18 } prtAlert
    
    # Basic SNMP attribute maps
    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.43.5.1.1.17.1': 'prtGeneralSerialNumber',
        '.1.3.6.1.2.1.43.10.2.1.2.1.1': 'prtMarkerMarkTech',
        '.1.3.6.1.2.1.43.10.2.1.6.1.1': 'numberColors',
    })

    ###########################################################################
    ### Text Conversions for represented integer values
    ###########################################################################

    # The type of marking technology used for this marking subunit
    PrtMarkerMarkTechTC = {
        1:  'other',
        2:  'unknown',
        3:  'LED',
        4:  'Laser',
        5:  'Other Electrophotographic',
        6:  '9-pin Dot Matrix',
        7:  '24-pin Dot Matrix',
        8:  'Other Dot Matrix',
        9:  'Impact Moving Head Fully Formed',
        10: 'Impact Band',
        11: 'Impact Other',
        12: 'Inkjet (Aqueous)',
        13: 'Inkjet (Solid)',
        14: 'Inkjet (Other)',
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
