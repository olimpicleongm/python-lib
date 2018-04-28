import AppKit, Foundation, objc

def notify(notificationTitle, notificationSubtitle, notificationText, withDelay=0, withSound=False, userInfo={}, imagePath=None):
	NSUserNotification = objc.lookUpClass('NSUserNotification')
	NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
	notification = NSUserNotification.alloc().init()
	notification.setTitle_(notificationTitle)
	notification.setSubtitle_(notificationSubtitle)
	notification.setInformativeText_(notificationText)
	notification.setUserInfo_(userInfo)
	if imagePath:
		#if os.path.exists(imagePath):
		try:
			contentImage = AppKit.NSImage.alloc().initByReferencingFile_(imagePath) #initByRerencingURL_(imageURL)
			notification.setContentImage_(contentImage)
		except:
			None
	if withSound:
		notification.setSoundName_('NSUserNotificationDefaultSoundName')
	notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(withDelay, Foundation.NSDate.date()))
	NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)