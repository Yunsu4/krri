package com.example.weddingappapi;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.util.ArrayList;

import network.RetrofitClient;
import network.RetrofitInterface;
import network.WeddingDataModel;
import network.WeddingModel;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    public static String TAG = "retrofit_test";
    //public static String buf = "";

    String SERVICE_KEY = "EH96GGOXuTBW0v0qyPE4TalwHts8X8ChekzRTYvaCky1UigpDM9YK6UQtH4wH1duKB3ZJDnMp4QZ0oOfegx42Q==";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);


        TextView tv = findViewById(R.id.text1);

        RetrofitInterface service = RetrofitClient.getInstance().create(RetrofitInterface.class);

        Call<WeddingModel> call = service.getServiceList(1,10,SERVICE_KEY);

        call.enqueue(new Callback<WeddingModel>() {
            @Override
            public void onResponse(Call<WeddingModel> call, Response<WeddingModel> response) {
                if(response.isSuccessful()){
                    Log.d(TAG, "연결 주소 확인: "+ response.raw().request().url().url());
                    Log.d(TAG, "통신여부 코드: "+ response.code());
                    WeddingModel wm = response.body();
                    assert wm != null;
                    ArrayList<WeddingDataModel> arr = wm.getData();
                    Log.d(TAG, "데이터 정보: "+wm.toString());

                    StringBuilder buf = new StringBuilder();
                    for (WeddingDataModel weddingDataModel : arr) {
                        buf.append(weddingDataModel.getServiceName()).append("\n");
                    }

                    //tv.setText(buf);
                    runOnUiThread(()-> tv.setText(buf.toString()));

                }
                else{
                    Log.e(TAG, "실패 코드 확인: "+ response.code());
                    Log.e(TAG, "연결 주소 확인: "+ response.raw().request().url().url());
                }
            }

            @Override
            public void onFailure(Call<WeddingModel> call, Throwable t) {
                Log.e(TAG, "onFailure: "+ t.getMessage());
            }
        });



    }
}