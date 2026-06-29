package com.algo.droid

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build

class BootReceiver : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
                    if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
                                    // फोन चालू झाल्यावर थेट Daemon Service सुरू करा
                                                val serviceIntent = Intent(context, AlgoDaemonService::class.java)
                                                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                                                                context.startForegroundService(serviceIntent)
                                                            } else {
                                                                                context.startService(serviceIntent)
                                                            }
                    }
        }
}

                                                            }
                                                            }
                    }
        }
}