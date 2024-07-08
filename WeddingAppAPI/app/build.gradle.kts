plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.example.weddingappapi"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.weddingappapi"
        minSdk = 21
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}

dependencies {

    implementation(libs.appcompat)
    implementation(libs.material)
    implementation(libs.activity)
    implementation(libs.constraintlayout)
    testImplementation(libs.junit)
    androidTestImplementation(libs.ext.junit)
    androidTestImplementation(libs.espresso.core)

    // Retrofit 라이브러리
    implementation ("com.squareup.retrofit2:retrofit:2.9.0")

    // Gson 변환기 라이브러리
    implementation ("com.squareup.retrofit2:converter-gson:2.9.0")

    // Scalars 변환기 라이브러리
    implementation ("com.squareup.retrofit2:converter-scalars:2.6.4")

    //json <-> 객체 변환하기 위해 사용
    implementation("com.google.code.gson:gson:2.8.7")
}