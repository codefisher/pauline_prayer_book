package au.org.paulinefathers.paulineprayerbook;

import android.app.ListActivity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.View;
import android.webkit.WebView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

public class IndexActivity extends ListActivity {

    public class MenuItem {
        protected String title;
        protected String doc;
        protected MenuItem[] children;

        public MenuItem(String aTitle, String aDoc) {
            title = aTitle;
            doc = aDoc;
            children = null;
        }

        public MenuItem(String aTitle, MenuItem[] aChildren) {
            title = aTitle;
            doc = null;
            children = aChildren;
        }

        public String getDoc() {
            return doc;
        }

        public MenuItem[] getChildren() {
            return children;
        }

        public String toString() {
            return title;
        }

    }

    ArrayAdapter<MenuItem> menuAdapter;
    ArrayList<ArrayAdapter<MenuItem>> menuAdapters = new ArrayList<ArrayAdapter<MenuItem>>();

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setUpMenu();
    }

    public void onBackPressed () {
        if(menuAdapters.isEmpty()) {
            finish();
        } else {
            menuAdapter = menuAdapters.remove(menuAdapters.size()-1);
            setListAdapter(menuAdapter);
        }
    }

    public void setUpMenu() {
        ArrayList<MenuItem> menuitems = null;
        XmlPullParserFactory pullParserFactory;
        try {
            pullParserFactory = XmlPullParserFactory.newInstance();
            XmlPullParser parser = pullParserFactory.newPullParser();
            String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
            InputStream in_s = getApplicationContext().getAssets().open("prayers/" + language + "/menu.xml");
            parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES, false);
            parser.setInput(in_s, null);

            menuitems = parseXML(parser);
            if(menuitems != null) {

                MenuItem[] menuitemsArray = menuitems.toArray(new MenuItem[menuitems.size()]);

                menuAdapter = new ArrayAdapter<MenuItem>(this, android.R.layout.simple_list_item_1, menuitemsArray);
                setListAdapter(menuAdapter);
            }

        } catch (XmlPullParserException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private ArrayList<MenuItem> parseXML(XmlPullParser parser) throws XmlPullParserException,IOException {
        ArrayList<MenuItem> menuitems = null;
        ArrayList<MenuItem> submenuitems = null;
        int eventType = parser.getEventType();
        MenuItem currentMenuItem = null;
        while (eventType != XmlPullParser.END_DOCUMENT) {
            String name = null;
            switch (eventType) {
                case XmlPullParser.START_DOCUMENT:

                    break;
                case XmlPullParser.START_TAG:
                    name = parser.getName();
                    if (name.equals("menu")) {
                        if(parser.getAttributeCount() == 0) {
                            menuitems = new ArrayList<MenuItem>();
                        } else {
                            String title = parser.getAttributeValue(0);
                            parser.next();
                            submenuitems = parseXML(parser);
                            if(submenuitems.size() != 0) {
                                MenuItem[] menuitemsArray = submenuitems.toArray(new MenuItem[submenuitems.size()]);
                                currentMenuItem = new MenuItem(title, menuitemsArray);
                                menuitems.add(currentMenuItem);
                            }
                        }
                    } else if (name.equals("menuitem")) {
                        if(menuitems == null) { // this happens in recursive call
                            menuitems = new ArrayList<MenuItem>();
                        }
                        String title = parser.getAttributeValue(0);
                        currentMenuItem = new MenuItem(title, parser.getAttributeValue(1));
                        menuitems.add(currentMenuItem);
                    }
                    break;
                case XmlPullParser.END_TAG:
                    name = parser.getName();
                    if(name != null && name.equals("menu")) {
                        parser.next();
                        return menuitems;
                    }
                    break;
            }
            eventType = parser.next();
        }
        return menuitems;
    }


    protected String getPrefSetting(String name, String defaultValue) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        return prefs.getString(name, defaultValue);
    }

    @Override
    protected void onListItemClick(ListView l, View v, int position, long id) {
        MenuItem item = (MenuItem)menuAdapter.getItem(position);
        if(item.getDoc() != null) {
            Intent intent = new Intent();
            intent.putExtra(PrayerActivity.EXTRA_DOC_NAME, item.getDoc());
            setResult(RESULT_OK, intent);
            finish();
        } else { // opens submenu
            menuAdapters.add(menuAdapter);
            menuAdapter = new ArrayAdapter<MenuItem>(this, android.R.layout.simple_list_item_1, item.getChildren());
            setListAdapter(menuAdapter);
        }
        super.onListItemClick(l, v, position, id);
    }
}