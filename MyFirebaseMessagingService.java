package com.test.prayertest;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;
import android.util.Log;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.os.Build;
import androidx.core.app.NotificationCompat;

public class MyFirebaseMessagingService extends FirebaseMessagingService {
    private static final String TAG = "FCMService";
    private static final String CHANNEL_ID = "prayer_notifications";

    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(TAG, "FirebaseMessagingService created");
        createNotificationChannel();
    }

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "Mesaj alindi from: " + remoteMessage.getFrom());

        // Data payload kontrolü
        if (remoteMessage.getData().size() > 0) {
            Log.d(TAG, "Data payload: " + remoteMessage.getData());
        }

        // Notification payload kontrolü
        if (remoteMessage.getNotification() != null) {
            String title = remoteMessage.getNotification().getTitle();
            String body = remoteMessage.getNotification().getBody();
            Log.d(TAG, "Notification Title: " + title);
            Log.d(TAG, "Notification Body: " + body);
            showNotification(title, body);
        }
    }

    @Override
    public void onNewToken(String token) {
        Log.d(TAG, "Yeni FCM token: " + token);
        // Burada token'ı backend'e gönderebilirsiniz
        // sendTokenToServer(token);
    }

    @Override
    public void onDeletedMessages() {
        Log.d(TAG, "onDeletedMessages called");
        super.onDeletedMessages();
    }

    @Override
    public void onMessageSent(String msgId) {
        Log.d(TAG, "Message sent: " + msgId);
        super.onMessageSent(msgId);
    }

    @Override
    public void onSendError(String msgId, Exception exception) {
        Log.e(TAG, "Send error: " + msgId, exception);
        super.onSendError(msgId, exception);
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "Prayer Notifications",
                NotificationManager.IMPORTANCE_HIGH
            );
            channel.setDescription("Namaz vakti bildirimleri");
            channel.enableLights(true);
            channel.enableVibration(true);
            
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) {
                manager.createNotificationChannel(channel);
                Log.d(TAG, "Notification channel created");
            }
        }
    }

    private void showNotification(String title, String message) {
        try {
            NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle(title != null ? title : "Prayer Test")
                .setContentText(message != null ? message : "Bildirim alındı")
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setAutoCancel(true)
                .setVibrate(new long[]{0, 500, 200, 500});

            NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            if (manager != null) {
                manager.notify((int) System.currentTimeMillis(), builder.build());
                Log.d(TAG, "Notification shown");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error showing notification", e);
        }
    }
}
