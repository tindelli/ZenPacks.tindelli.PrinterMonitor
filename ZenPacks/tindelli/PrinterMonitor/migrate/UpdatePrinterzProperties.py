
PROP_zPythonClass = "zPythonClass"
PROP_zSnmpMonitorIgnore = "zSnmpMonitorIgnore"
PROP_zCollectorPlugins = "zCollectorPlugins"
DEVICECLASS = "/Printer"
FROM_zPythonClasses = ("", "Products.ZenModel.Device")
TO_zPythonClass = "ZenPacks.tindelli.PrinterMonitor.PrinterDevice"
MODELER_PLUGINS = [
    'tindelli.snmp.PrinterMonitor',
    'zenoss.snmp.NewDeviceMap',
    'zenoss.snmp.DeviceMap']


import logging
LOG = logging.getLogger('zen.migrate')

from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration

from ZenPacks.tindelli.PrinterMonitor.PrinterDevice import PrinterDevice

class UpdatePrinterzProperties(ZenPackMigration):
    """Update zProperties for /Printer device class."""

    version = Version(1, 0, 0)

    def migrate(self, dmd):

        try:
            deviceclass = dmd.Devices.getOrganizer(DEVICECLASS)
        except Exception:
            return

        if deviceclass.getZ(PROP_zPythonClass) != TO_zPythonClass:
            LOG.info(
                "changing %s %s to %s",
                deviceclass.getOrganizerName(),
                PROP_zPythonClass,
                TO_zPythonClass)

            deviceclass.setZenProperty(PROP_zPythonClass, TO_zPythonClass)

        if not deviceclass.hasProperty(PROP_zSnmpMonitorIgnore):
            LOG.info(
                "Setting explicit %s override on %s",
                PROP_zSnmpMonitorIgnore,
                deviceclass.getOrganizerName())
            deviceclass.setZenProperty(PROP_zSnmpMonitorIgnore, True)
            deviceclass.setZenProperty(PROP_zSnmpMonitorIgnore, False)

        LOG.info(
            "Updating %s of %s",
            PROP_zCollectorPlugins,
            deviceclass.getOrganizerName())

        deviceclass.setZenProperty(PROP_zCollectorPlugins, MODELER_PLUGINS)

        LOG.info(
            "Reclassifying devices as %s",
            TO_zPythonClass)

        for device in deviceclass.getSubDevicesGen():
            if not isinstance(device, PrinterDevice):
                deviceclass.moveDevices(
                    device.deviceClass().getOrganizerName(),
                    device.id)

                device.buildRelations()

        LOG.info("Finished converting devices.")

UpdatePrinterzProperties()