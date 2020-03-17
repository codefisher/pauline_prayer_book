package au.org.paulinefathers.paulineprayerbook;

import android.os.Bundle;
import androidx.preference.PreferenceFragmentCompat;

public class AppSettingsFragment extends PreferenceFragmentCompat {
    @Override
    public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
        setPreferencesFromResource(R.xml.preferences, rootKey);
    }
}
