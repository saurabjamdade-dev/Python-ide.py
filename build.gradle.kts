plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
    // नियम ३ व १८: जड आणि हलक्या पायथन लायब्ररी चालवण्यासाठी CPython प्लगिन
    id("com.chaquo.python") version "15.0.1" apply false
}

tasks.register<Delete>("clean") {
    delete(rootProject.buildDir)
}
