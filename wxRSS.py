import feedparser
import os
import unidecode
import wx
import wx.html2 as webview

from ObjectListView import ObjectListView, ColumnDefn


########################################################################
class RSS(object):
    """
    RSS object
    """

    # ----------------------------------------------------------------------
    def __init__(self, title, link, website, summary, all_data):
        """Constructor"""
        self.title = title
        self.link = link
        self.all_data = all_data
        self.website = website
        self.summary = summary


########################################################################
class RssPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.data = []

        lbl = wx.StaticText(self, label="Feed URL:")
        self.rssUrlTxt = wx.TextCtrl(self, value="http://www.blog.pythonlibrary.org/feed/")
        urlBtn = wx.Button(self, label="Get Feed")
        urlBtn.Bind(wx.EVT_BUTTON, self.get_data)

        self.rssOlv = ObjectListView(self,
                                     style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.rssOlv.SetEmptyListMsg("No data")
        self.rssOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.rssOlv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_double_click)
        self.summaryTxt = webview.WebView.New(self)

        self.wv = webview.WebView.New(self)

        # add sizers
        rowSizer = wx.BoxSizer(wx.HORIZONTAL)
        rowSizer.Add(lbl, 0, wx.ALL, 5)
        rowSizer.Add(self.rssUrlTxt, 1, wx.EXPAND | wx.ALL, 5)
        rowSizer.Add(urlBtn, 0, wx.ALL, 5)

        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.rssOlv, 1, wx.EXPAND | wx.ALL, 5)
        vSizer.Add(self.summaryTxt, 1, wx.EXPAND | wx.ALL, 5)

        dispSizer = wx.BoxSizer(wx.HORIZONTAL)
        dispSizer.Add(vSizer, 1, wx.EXPAND | wx.ALL, 5)
        dispSizer.Add(self.wv, 2, wx.EXPAND | wx.ALL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(rowSizer, 0, wx.EXPAND)
        mainSizer.Add(dispSizer, 1, wx.EXPAND)
        self.SetSizer(mainSizer)

        self.update_display()

    # ----------------------------------------------------------------------
    def get_data(self, event):
        """
        Get RSS feed and add it to display
        """
        msg = "Processing feed..."
        busyDlg = wx.BusyInfo(msg)
        rss = self.rssUrlTxt.GetValue()
        feed = feedparser.parse(rss)

        website = feed["feed"]["title"]
        for key in feed["entries"]:
            title = unidecode.unidecode(key["title"])
            link = key["link"]
            summary = key["summary"]
            self.data.append(RSS(title, link, website, summary, key))

        busyDlg = None
        self.update_display()

    # ----------------------------------------------------------------------
    def on_double_click(self, event):
        """
        Load the selected link in the browser widget
        """
        obj = self.rssOlv.GetSelectedObject()
        self.wv.LoadURL(obj.link)

    # ----------------------------------------------------------------------
    def on_select(self, event):
        """
        Load the summary in the text control
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        obj = self.rssOlv.GetSelectedObject()
        html = "<html><body>%s</body></html>" % obj.summary
        fname = "summary.html"
        full_path = os.path.join(base_path, fname)
        try:
            with open(full_path, "w") as fh:
                fh.write(html)
                print
                "file:///" + full_path
                self.summaryTxt.LoadURL("file:///" + full_path)
        except (OSError, IOError):
            print
            "Error writing html summary"

    # ----------------------------------------------------------------------
    def update_display(self):
        """
        Update the RSS feed display
        """
        self.rssOlv.SetColumns([
            ColumnDefn("Title", "left", 200, "title"),
            ColumnDefn("Website", "left", 200, "website"),
        ])
        self.rssOlv.SetObjects(self.data)


########################################################################
class RssFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="RSS Reader", size=(1200, 800))
        panel = RssPanel(self)
        self.Show()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = RssFrame()
    app.MainLoop()