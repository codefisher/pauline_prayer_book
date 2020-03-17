package au.org.paulinefathers.paulineprayerbook;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.preference.PreferenceManager;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.print.PrintAttributes;
import android.print.PrintDocumentAdapter;
import android.print.PrintJob;
import android.print.PrintManager;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class PrayerActivity extends AppCompatActivity implements SharedPreferences.OnSharedPreferenceChangeListener {

    Integer OPTIONS_REQUEST_CODE = 109;
    public final static String EXTRA_DOC_NAME = "au.org.paulinefathers.paulineprayerbook.doc";

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

    MediaPlayer mediaPlayer = null;

    @JavascriptInterface
    public void play(String name) {
        if(mediaPlayer != null) {
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
        int resourceID = getResources().getIdentifier(name.replace('-', '_'), "raw", getPackageName());
        if(resourceID != 0) {
            mediaPlayer = MediaPlayer.create(this, resourceID);

            if (mediaPlayer != null) {
                mediaPlayer.start();
            }
        }
    }

    @JavascriptInterface
    public void stop() {
        if(mediaPlayer != null) {
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prayer);

        NotificationEventReceiver.setupAlarm(getApplicationContext());

        WebView webView = (WebView) findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.addJavascriptInterface(new JsPrefObject(), "prefObject");
        webView.addJavascriptInterface(this, "chantPlayer");


        WebSettings webSettings = webView.getSettings();
        webSettings.setDefaultFontSize(Integer.parseInt(getPrefSetting("font_size_list", getString(R.string.pref_font_size_default))));
        webSettings.setDefaultTextEncodingName("utf-8");

        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        webSettings.setAllowFileAccessFromFileURLs(true);
        webSettings.setAllowUniversalAccessFromFileURLs(true);

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

            public void onPageFinished(WebView view, String url) {
                if(getPrefSetting("dark_mode", false)) {
                    view.loadUrl(
                            "javascript:document.body.classList.add('darktheme');"
                    );
                }
            }
        });

        /* this will happen when opening notification */
        Intent intent = getIntent();
        if(intent != null) {
            String doc = intent.getStringExtra(EXTRA_DOC_NAME);
            if(doc != null) {
                webView.loadUrl("file:///android_asset/prayers/" + language + "/" + doc);
                return;
            }
        }

        /* the normal startup */
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
    public void onDestroy() {
        if (mediaPlayer != null) {
            mediaPlayer.release();
        }
        super.onDestroy();
    }

    public void onBackPressed () {
        WebView webView = (WebView) findViewById(R.id.webView);
        if(webView.canGoBack()) {
            webView.goBack();
        } else {
            finish();
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
        } else if (key.equals("dark_mode")) {
            WebView webView = (WebView) findViewById(R.id.webView);
            if(getPrefSetting("dark_mode", false)) {
                webView.loadUrl(
                        "javascript:document.body.classList.add('darktheme');"
                );
            } else {
                webView.loadUrl(
                        "javascript:document.body.classList.remove('darktheme');"
                );
            }
        }
        // handle the preference change here
    }

    protected String getPrefSetting(String name, String defaultValue) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String rs = prefs.getString(name, defaultValue);
        return rs;
    }

    protected Boolean getPrefSetting(String name, Boolean defaultValue) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        Boolean rs = prefs.getBoolean(name, defaultValue);
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

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        try {
            if (requestCode == OPTIONS_REQUEST_CODE && data.hasExtra(EXTRA_DOC_NAME)) {
                String doc = data.getStringExtra(EXTRA_DOC_NAME);
                WebView webView = (WebView) findViewById(R.id.webView);
                String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
                webView.loadUrl("file:///android_asset/prayers/" + language + "/" + doc);
            }
        } catch (NullPointerException e) {
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
                startActivityForResult(intent, OPTIONS_REQUEST_CODE);
                return true;
            case R.id.action_about:
                WebView webView = (WebView) findViewById(R.id.webView);
                String language = getPrefSetting("language_list", getString(R.string.pref_language_default));
                webView.loadUrl("file:///android_asset/prayers/" + language + "/about.html");
                return true;
            case R.id.action_print:
                createWebPrintJob();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    private void createWebPrintJob() {

        // Get a PrintManager instance
        PrintManager printManager = (PrintManager)this.getSystemService(Context.PRINT_SERVICE);

        String jobName = getString(R.string.app_name);

        // Get a print adapter instance
        WebView webView = (WebView) findViewById(R.id.webView);
        PrintDocumentAdapter printAdapter = webView.createPrintDocumentAdapter(jobName);

        // Create a print job with name and adapter instance
        PrintJob printJob = printManager.print(jobName, printAdapter,
                new PrintAttributes.Builder().build());
    }


}
