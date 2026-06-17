package com.algodroid.pro

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat
import com.chaquo.python.Python

class AlgoDaemonService : Service() {

    private var wakeLock: PowerManager.WakeLock? = null
    private var isServiceRunning = false

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        
        // नियम ८: अँड्रॉइड वेकलॉक ॲक्टिव्हेट करणे (सिस्टीम ऑप्टिमायझेशन टाळण्यासाठी)
        val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AlgoDroid::DaemonWakeLock")
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (!isServiceRunning) {
            isServiceRunning = true
            
            // वेकलॉक लॉक करणे जेणेकरून स्क्रीन बंद झाल्यावरही सिस्टीम मरत नाही
            wakeLock?.acquire()

            // बॅकग्राउंड नोटिफिकेशन सुरू करणे
            val notification = createNotification("AlgoDroid Pro Background Engine Active 24/7")
            startForeground(101, notification)

            // नियम २०: स्वतंत्र डॅमन थ्रेडवर पायथन लाइव्ह रनर सुरू करणे
            Thread {
                runPersistentPythonEngine()
            }.start()
        }
        return START_STICKY // सिस्टीमने चुकून सर्व्हिस बंद केली तर आपोआप रीस्टार्ट होईल
    }

    private fun runPersistentPythonEngine() {
        try {
            // नियम २ आणि १३: CPython बॅकएंड लेअर रनर
            val py = Python.getInstance()
            val pyModule = py.getModule("app_backend")
            
            // पायथनच्या अंतर्गत लूपला ट्रिगर करणे जे २४ तास चालेल
            pyModule.callAttr("start_daemon_loop")
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun createNotification(content: String): Notification {
        return NotificationCompat.Builder(this, "algodroid_daemon_channel")
            .setContentTitle("AlgoDroid Pro")
            .setContentText(content)
            .setSmallIcon(android.R.drawable.ic_media_play)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_MIN)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "algodroid_daemon_channel",
                "AlgoDroid Daemon Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (wakeLock?.isHeld == true) {
            wakeLock?.release()
        }
        isServiceRunning = false
    }
}
