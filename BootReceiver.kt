package com.algodroid.pro

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        // नियम २१: फोन चालू होताच बॅकग्राउंड डॅमन प्रोसेस पुन्हा सुरू करणे
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val serviceIntent = Intent(context, AlgoExecutionService::class.java).apply {
                putExtra("SCRIPT_NAME", "Auto_Restart_Daemon_Active.py")
            }
            context.startForegroundService(serviceIntent)
        }
    }
}
