package au.org.paulinefathers.paulineprayerbook;

import android.app.IntentService;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Build;
import android.preference.PreferenceManager;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.legacy.content.WakefulBroadcastReceiver;

import org.json.JSONException;

import java.io.IOException;
import java.util.Calendar;
import java.util.Date;

public class NotificationIntentService extends IntentService {

    private static final int NOTIFICATION_ID = 1;
    private static final String ACTION_START = "ACTION_START";
    private static final String ACTION_DELETE = "ACTION_DELETE";

    private static final String NOTIFICATION_CHANNEL_ID_TODAY = "PAULINE_PRAYER_BOOK_NOTIFICATION_TODAY";
    private static final String NOTIFICATION_CHANNEL_ID_TOMORROW = "PAULINE_PRAYER_BOOK_NOTIFICATION_TOMORROW";


    public NotificationIntentService() {
        super(NotificationIntentService.class.getSimpleName());
    }

    public static Intent createIntentStartNotificationService(Context context) {
        Intent intent = new Intent(context, NotificationIntentService.class);
        intent.setAction(ACTION_START);
        return intent;
    }

    public static Intent createIntentDeleteNotification(Context context) {
        Intent intent = new Intent(context, NotificationIntentService.class);
        intent.setAction(ACTION_DELETE);
        return intent;
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        Log.d(getClass().getSimpleName(), "onHandleIntent, started handling a notification event");
        try {
            String action = intent.getAction();
            if (ACTION_START.equals(action)) {
                processStartNotification();
            }
            if (ACTION_DELETE.equals(action)) {
                processDeleteNotification(intent);
            }
        } finally {
            WakefulBroadcastReceiver.completeWakefulIntent(intent);
        }
    }

    private void processDeleteNotification(Intent intent) {
        // Log something?
    }

    protected String getPrefSetting(String name, String defaultValue) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String rs = prefs.getString(name, defaultValue);
        return rs;
    }

    private void sendNotification(String title, String description, String doc, String ChannelID) {
        final NotificationCompat.Builder builder = new NotificationCompat.Builder(this, ChannelID);
        builder.setContentTitle(title)
                .setAutoCancel(true)
                .setColor(getResources().getColor(R.color.colorAccent))
                .setContentText(description)
                .setSmallIcon(R.mipmap.ic_launcher);
        Intent intent = new Intent(this, PrayerActivity.class);
        if(doc != null) {
            intent.putExtra(PrayerActivity.EXTRA_DOC_NAME, doc);
        }
        PendingIntent pendingIntent = PendingIntent.getActivity(this,
                NOTIFICATION_ID,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT);
        builder.setContentIntent(pendingIntent);
        builder.setDeleteIntent(NotificationEventReceiver.getDeleteIntent(this));

        final NotificationManager manager = (NotificationManager) this.getSystemService(Context.NOTIFICATION_SERVICE);
        manager.notify(NOTIFICATION_ID, builder.build());
    }

    private void createChanel(String channelID) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = getString(R.string.channel_name);
            String description = getString(R.string.channel_description);
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(channelID, name, importance);
            channel.setDescription(description);
            // Register the channel with the system; you can't change the importance
            // or other notification behaviors after this
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }

    private void processStartNotification() {

        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        if(!prefs.getBoolean("notifications", true)) {
            return;
        }

        createChanel(NOTIFICATION_CHANNEL_ID_TODAY);
        createChanel(NOTIFICATION_CHANNEL_ID_TOMORROW);

        Calendar today = Calendar.getInstance();
        today.setTime(new Date());

        try {
            PaulineCalendar calendar = new PaulineCalendar(today.get(Calendar.YEAR), getApplicationContext());

            String name = calendar.getName(today);
            if(name != null) {
                String link = calendar.getLink(today);
                String type = calendar.getType(today);
                if(type != null) {
                     name = name + ", " + type;
                }
                sendNotification(getString(R.string.today_feast), name, link, NOTIFICATION_CHANNEL_ID_TODAY);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            Calendar tomorrow = Calendar.getInstance();
            tomorrow.setTime(new Date());
            tomorrow.add(Calendar.DAY_OF_YEAR, 1);

            String nameTomorrow = calendar.getName(tomorrow);
            if(nameTomorrow != null) {
                String linkTomorrow = calendar.getLink(tomorrow);
                String typeTomorrow = calendar.getType(tomorrow);
                if(typeTomorrow != null) {
                    nameTomorrow = nameTomorrow + ", " + typeTomorrow;
                }
                sendNotification(getString(R.string.tommorrow_feast), nameTomorrow, linkTomorrow, NOTIFICATION_CHANNEL_ID_TOMORROW);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}

