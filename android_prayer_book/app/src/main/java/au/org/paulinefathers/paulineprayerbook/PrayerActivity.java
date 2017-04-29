package au.org.paulinefathers.paulineprayerbook;

import android.content.Intent;
import android.content.SharedPreferences;
import android.net.MailTo;
import android.net.Uri;
import android.os.Build;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class PrayerActivity extends AppCompatActivity implements SharedPreferences.OnSharedPreferenceChangeListener {

    Integer OPTIONS_REQUEST_CODE = 109;
    String EXTRA_DOC_NAME = "au.org.paulinefathers.paulineprayerbook.doc";

    class JsPrefObject {

        @JavascriptInterface
        public String get(String name, String def) {
            String rs =  getPrefSetting(name, def);
            return rs;
        }

        @JavascriptInterface
        public void set(String name, String value) {
            setPrefSetting(name, value);
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prayer);

        WebView webView = (WebView) findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.addJavascriptInterface(new JsPrefObject(), "prefObject");

        WebSettings webSettings = webView.getSettings();
        webSettings.setDefaultFontSize(Integer.parseInt(getPrefSetting("font_size_list", getString(R.string.pref_font_size_default))));
        webSettings.setDefaultTextEncodingName("utf-8");

        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
            webSettings.setAllowFileAccessFromFileURLs(true);
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
            webSettings.setAllowUniversalAccessFromFileURLs(true);
        }

        String language = getPrefSetting("language_list", getString(R.string.pref_language_default));

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                if(description.equals("net::ERR_FILE_NOT_FOUND") && !failingUrl.endsWith("front.html")) {
                    String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
                    view.loadUrl("file:///android_asset/prayers/" + language + "/front.html");
                }
            }
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url)
            {
                if (url.startsWith("http://") || url.startsWith("mailto:")) {
                    Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    startActivity(browserIntent);
                    return true;
                }
                return false;
            }
        });

        PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).registerOnSharedPreferenceChangeListener(this);
        if (savedInstanceState != null) {
            String currentPage = savedInstanceState.getString("current_page");
            if(currentPage != null) {
                webView.loadUrl(currentPage);
            } else {
                webView.loadUrl("file:///android_asset/prayers/" + language + "/front.html");
            }
        } else {
            webView.loadUrl("file:///android_asset/prayers/" + language + "/front.html");
        }
    }

    @Override
    public void onSaveInstanceState(Bundle out) {
        WebView webView = (WebView) findViewById(R.id.webView);
        out.putString("current_page", webView.getUrl());
        super.onSaveInstanceState(out);
    }

    @Override
    public void onRestoreInstanceState(Bundle savedInstanceState) {
        WebView webView = (WebView) findViewById(R.id.webView);
        webView.loadUrl(savedInstanceState.getString("current_page"));
    }


    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key) {
        if(key.equals("font_size_list")){
            WebView webView = (WebView) findViewById(R.id.webView);
            WebSettings webSettings = webView.getSettings();
            webSettings.setDefaultFontSize(Integer.parseInt(getPrefSetting("font_size_list", getString(R.string.pref_font_size_default))));
        } else if(key.equals("language_list")) {
            String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
            WebView webView = (WebView) findViewById(R.id.webView);
            webView.loadUrl("file:///android_asset/prayers/" + language + "/front.html");
        }
        // handle the preference change here
    }

    protected String getPrefSetting(String name, String defaultValue) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String rs = prefs.getString(name, defaultValue);
        return rs;
    }

    protected void setPrefSetting(String name, String value) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString(name, value);
        editor.apply();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main_menu, menu);
        return true;
    }

    protected void onActivityResult (int requestCode, int resultCode, Intent data) {
        try {
            if(requestCode == OPTIONS_REQUEST_CODE && data.hasExtra(EXTRA_DOC_NAME)) {
                String doc = data.getStringExtra(EXTRA_DOC_NAME);
                WebView webView = (WebView) findViewById(R.id.webView);
                String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
                webView.loadUrl("file:///android_asset/prayers/" + language + "/" + doc);
            }
        } catch (NullPointerException e ) {
            // happens when the back button is pressed without selecting anything
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.action_settings:
                startActivity(new Intent(this, SettingsActivity.class));
                return true;
            case R.id.action_index:
                Intent intent = new Intent(this, IndexActivity.class);
                int requestCode = 109;
                startActivityForResult(intent, requestCode);
                return true;
            case R.id.action_about:
                WebView webView = (WebView) findViewById(R.id.webView);
                String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
                webView.loadUrl("file:///android_asset/prayers/" + language + "/about.html");
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }


}
