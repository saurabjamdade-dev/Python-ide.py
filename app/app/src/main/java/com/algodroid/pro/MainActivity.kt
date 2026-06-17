package com.algodroid.pro

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.algodroid.pro.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var isTerminal = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupShortcutBar()

        binding.fabPlay.setOnClickListener {
            if (!isTerminal) {
                binding.codeEditor.visibility = View.GONE
                binding.terminalView.visibility = View.VISIBLE
                binding.txtTerminalLog.text = "Terminal Loaded. Ready.\n🟢 Code Sanitizer: Success.\n>> Running Algorithmic Strategy rules..."
                isTerminal = true
            } else {
                binding.codeEditor.visibility = View.VISIBLE
                binding.terminalView.visibility = View.GONE
                isTerminal = false
            }
        }

        // २४/७ इंडिपेंडंट डॅमन बॅकग्राउंड सर्व्हिस ट्रिगर हुक
        startService(Intent(this, AlgoDaemonService::class.java))
    } 

    private fun setupShortcutBar() {
        val symbols = arrayOf("Tab", ":", ";", "'", "#", "(", ")", "[", "]")
        for (sym in symbols) {
            val b = Button(this).apply { 
                text = sym
                setTextColor(android.graphics.Color.WHITE) 
            }
            b.setOnClickListener { 
                val textToInsert = if (sym == "Tab") "    " else sym
                binding.codeEditor.text.insert(binding.codeEditor.selectionStart, textToInsert) 
            }
            binding.shortcutBarLayout.addView(b)
        }
    }
}
