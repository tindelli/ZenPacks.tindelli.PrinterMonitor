
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

try:
	from Products.ZenUtils.events import pausedAndOptimizedReindexing
except ImportError:
	def pausedAndOptimizedReindexing():
		yield

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

#		with pausedAndOptimizedReindexing:
#			for device in deviceclass.getSubDevicesGen():
#				if not isinstance(device, PrinterDevice):
#					reclass_device(device, PrinterDevice)

#					device.buildRelations()

		LOG.info("Finished converting devices.")


#def reclass_device(device, klass):
	"""Change the __class__ of device to klass.

    This isn't quite as simple as "device.__class__ = klass" because ZODB
    stores the class in the persistent reference to the object, not in the
    object itself. As soon as the container is loaded from the ZODB, a ghost is
    created for its persistent reference using the class mentioned there.

    This function works around this issue by also replacing the persistent
    reference to the object after changing it's __class__.

    See the following article for the inspiration for this function.

    http://blog.redturtle.it/2013/02/25/migrating-dexterity-items-to-dexterity-containers

    """
    # For example: dmd.Devices.Server.SSH.Linux.devices._objects
#    container = device.getPrimaryParent()._objects

    # Get the unwrapped object.
#    unwrapped_device = container[device.id]

    # Delete the object's persistent reference.
#    del container[unwrapped_device.id]

    # Change the unwrapped object's class.
#    unwrapped_device.__class__ = klass

    # Add back a persistent reference to the newly-classed object.
#    container[unwrapped_device.id] = unwrapped_device

UpdatePrinterzProperties()