plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.chaquo.python") // नियम २: CPython इंजिन ॲक्टिव्हेशन
}

android {
    namespace = "com.algodroid.pro"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.algodroid.pro"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        
        // नियम ३, १८: पायथन लायब्ररी मॅनेजर सेटअप (Pip Package Manager Engine)
        ndk {
            abiFilters.addAll(setOf("armeabi-v7a", "arm64-v8a", "x86", "x86_64"))
        }

        python {
            version = "3.12" // कडक CPython ३.१२ इंजिन
            pip {
                // तुमच्या मार्केट आणि क्रिप्टो ट्रेडिंगसाठी लागणाऱ्या गाभ्याच्या लायब्ररीज
                install("pandas")
                install("numpy")
                install("ccxt")
                install("yfinance")
                install("numba")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        viewBinding = true // नियम २२: Pydroid 3 सारखा वेगवान इंटरफेस बनवण्यासाठी
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    
    // नियम १५: Google Drive आणि File API सोयीसाठी लायब्ररीज
    implementation("com.google.android.gms:play-services-auth:20.7.0")
}
