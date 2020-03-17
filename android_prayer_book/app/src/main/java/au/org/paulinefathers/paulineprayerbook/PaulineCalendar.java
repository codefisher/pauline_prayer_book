package au.org.paulinefathers.paulineprayerbook;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class PaulineCalendar {

    int year;
    Context context;
    JSONObject calendarData;

    public PaulineCalendar(int year, Context context) throws IOException, JSONException {
        this.year = year;
        this.context = context;

        String json = loadJSONFromAsset();
        calendarData = new JSONObject(json);

        Calendar easter = easter(year);

        Calendar motherChurch = Calendar.getInstance();
        motherChurch.setTime(easter.getTime());
        motherChurch.add(Calendar.DAY_OF_YEAR, 50);
        calendarData.put(formatDate(motherChurch), calendarData.get("mother-church"));

        Calendar stPaul = Calendar.getInstance();
        stPaul.set(year, 0, 15);
        if(stPaul.get(Calendar.DAY_OF_WEEK) == Calendar.SUNDAY) {
            Calendar novena = Calendar.getInstance();
            novena.setTime(stPaul.getTime());
            novena.add(Calendar.DAY_OF_YEAR, -9);
            calendarData.put(formatDate(novena), calendarData.get("paul-novena"));
        } else {
            int diff = 7 - (stPaul.get(Calendar.DAY_OF_WEEK) - 1);
            Calendar external = Calendar.getInstance();
            external.setTime(stPaul.getTime());
            external.add(Calendar.DAY_OF_YEAR, diff);
            calendarData.put(formatDate(external), calendarData.get("paul-external"));

            Calendar novena = Calendar.getInstance();
            novena.setTime(external.getTime());
            novena.add(Calendar.DAY_OF_YEAR, -9);
            calendarData.put(formatDate(novena), calendarData.get("paul-novena"));
        }

        Calendar consecration = Calendar.getInstance();
        consecration.set(year, 9, 31);
        if(stPaul.get(Calendar.DAY_OF_WEEK) != Calendar.SUNDAY) {
            int diff = (consecration.get(Calendar.DAY_OF_WEEK) - 1);
            consecration.add(Calendar.DAY_OF_YEAR, -diff);
        }
        calendarData.put(formatDate(consecration), calendarData.get("church-consecration"));
    }

    public String loadJSONFromAsset() throws IOException {
        String json = null;
        String language = getPrefSetting("language_list", this.context.getString(R.string.pref_language_default));
        InputStream is = this.context.getAssets().open("prayers/" + language + "/feasts.json");
        int size = is.available();
        byte[] buffer = new byte[size];
        is.read(buffer);
        is.close();
        json = new String(buffer, "UTF-8");
        return json;
    }

    protected JSONObject getFeast(Calendar date) throws JSONException {
        return calendarData.getJSONObject(formatDate(date));
    }

    public String getLink(Calendar date) {
        try {
            return getFeast(date).getString("link");
        } catch (JSONException e) {
            return null;
        }
    }

    public String getName(Calendar date) {
        try {
            return getFeast(date).getString("name");
        } catch (JSONException e) {
            return null;
        }
    }

    public String getType(Calendar date) {
        try {
            return getFeast(date).getString("type");
        } catch (JSONException e) {
            return null;
        }
    }

    protected String formatDate(Calendar date) {
        String month = String.format(Locale.ENGLISH, "%02d", (date.get(Calendar.MONTH) + 1));
        String day = String.format(Locale.ENGLISH,"%02d", (date.get(Calendar.DAY_OF_MONTH)));
        return month + day;
    }

    protected String getPrefSetting(String name, String defaultValue) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this.context);
        String rs = prefs.getString(name, defaultValue);
        return rs;
    }

    public Calendar easter(int year) {
        // Golden Number - 1
        double G = year % 19;
        double C = Math.floor((double)year / 100);
        // related to Epact
        double H = ((C - Math.floor(C / 4) - Math.floor((8 * C + 13)/25) + 19 * G + 15) % 30);
        // number of days from 21 March to the Paschal full moon
        double I = H - Math.floor(H/28) * (1 - Math.floor(29/(H + 1)) * Math.floor((21-G)/11));
        // weekday for the Paschal full moon
        double J = (year + Math.floor((double)year / 4) + I + 2 - C + Math.floor(C / 4)) % 7;
        // number of days from 21 March to the Sunday on or before the Paschal full moon
        double L = I - J;
        int month = (int) (3 + Math.floor((L + 40)/44));
        int day = (int) (L + 28 - 31 * Math.floor((double)month / 4));

        Calendar result = Calendar.getInstance();
        result.set(year, month, day);

        return result;
    }
}
