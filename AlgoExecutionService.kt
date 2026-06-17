package com.algodroid.pro

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat

class AlgoExecutionService : Service() {
    private var wakeLock: PowerManager.WakeLock? = null
    private val CHANNEL_ID = "AlgoDroidExecutionChannel"

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        acquireWakeLock()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val scriptName = intent?.getStringExtra("SCRIPT_NAME") ?: "Unknown Strategy"

        // नियम २३ आणि २४: स्क्रीन लॉक झाल्यावरही अखंड चालू राहणारे परसिस्टंट नोटिफिकेशन
        val notification: Notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("AlgoDroid Pro Engine Active")
            .setContentText("Running: $scriptName (Infinite Subprocess)")
            .setSmallIcon(android.R.drawable.ic_media_play)
            .setOngoing(true)
            .build()

        // Android 14/15 नियमांनुसार FOREGROUND_SERVICE सुरू करणे
        startForeground(101, notification)

        // येथे तुमचा CPython मॅनेजर/सबप्रोसेस स्वतंत्र थ्रेडवर रन होईल
        Thread {
            try {
                while (wakeLock?.isHeld == true) {
                    // बॅकग्राउंड नेटवर्क पोल्स आणि एक्झिक्युशन इंजिन स्लीप लूप
                    Thread.sleep(10000)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()

        return START_STICKY // सिस्टीमने मेमरी अभावी किल केले तर ऑटो-रिस्टार्ट करा
    }

    private fun acquireWakeLock() {
        val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
        // नियम ८: स्क्रीन लॉक आणि डोझ मोड (Doze Mode) मध्येही CPU चालू ठेवणे
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AlgoDroid::TradingWakeLock")
        wakeLock?.acquire()
    }

    private fun createNotificationChannel() {
        val serviceChannel = NotificationChannel(
            CHANNEL_ID,
            "AlgoDroid Persistent Service",
            NotificationManager.IMPORTANCE_LOW
        )
        val manager = getSystemService(NotificationManager::class.java)
        manager?.createNotificationChannel(serviceChannel)
    }

    override fun onDestroy() {
        if (wakeLock?.isHeld == true) {
            wakeLock?.release()
        }
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
