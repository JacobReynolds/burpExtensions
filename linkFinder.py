# Burp Extension - Link Finder
# Copyright : Jake Reynolds (jreynoldsdev@gmail.com)
#This burp extension will parse all hyperlinks from an HTTP response and aggregate
#them into a separate 'Link Finder' tab

#Modeled after JSONDecoder by: Michal Melewski <michal.melewski@gmail.com>

import json
import re

from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()

		callbacks.setExtensionName('Link Finder')
		callbacks.registerMessageEditorTabFactory(self)

		return

	def createNewInstance(self, controller, editable):
		return LinkFinderTab(self, controller, editable)

class LinkFinderTab(IMessageEditorTab):
	def __init__(self, extender, controller, editable):
		self._extender = extender
		self._helpers = extender._helpers
		self._editable = editable

		self._txtInput = extender._callbacks.createTextEditor()
		self._txtInput.setEditable(editable)

		return

	def getTabCaption(self):
		return "Link Finder"

	def getUiComponent(self):
		return self._txtInput.getComponent()

	def isEnabled(self, content, isRequest):
		r = self._helpers.analyzeResponse(content)
		msg = content[r.getBodyOffset():].tostring()
		links = re.findall(r'href=[\'"]?([^\'" >]+)', msg)
		return len(links) != 0

	def setMessage(self, content, isRequest):
		if content is None:
			self._txtInput.setText(None)
			self._txtInput.setEditable(False)
		else:
			r = self._helpers.analyzeResponse(content)
			msg = content[r.getBodyOffset():].tostring()
			#Need to get host here, and then make links clickable
			links = re.findall(r'href=[\'"]?([^\'" >]+)', msg)
			links = '\n'.join(links)
			self._txtInput.setText(links)
			self._currentMessage = links

	def getMessage(self):
		return self._currentMessage

	def isModified(self):
		return self._txtInput.isTextModified()

	def getSelectedData(self):
		return self._txtInput.getSelectedText()
