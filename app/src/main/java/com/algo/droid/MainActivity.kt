<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#121212">

    <WebView
        android:id="@+id/editorWebView"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="0.7" />

    <View
        android:layout_width="match_parent"
        android:layout_height="2dp"
        android:background="#333333" />

    <RelativeLayout
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="0.3"
        android:background="#000000">

        <ScrollView
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:padding="8dp">
            <TextView
                android:id="@+id/consoleOutput"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:textColor="#00FF00"
                android:textSize="13sp"
                android:fontFamily="monospace"
                android:text="> Algo Droid Terminal...\n" />
        </ScrollView>

        <Button
            android:id="@+id/btnRun"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_alignParentBottom="true"
            android:layout_alignParentEnd="true"
            android:layout_margin="16dp"
            android:backgroundTint="#FFDD00"
            android:textColor="#000000"
            android:textStyle="bold"
            android:text="▶ RUN" />
    </RelativeLayout>
</LinearLayout>
