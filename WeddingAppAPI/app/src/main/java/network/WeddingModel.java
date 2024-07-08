package network;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;

public class WeddingModel {

    @SerializedName("page")
    @Expose
    private int page;

    @SerializedName("perPage")
    @Expose
    private int perPage;

    @SerializedName("data")
    @Expose
    private ArrayList<WeddingDataModel> data;


    public int getPage() {
        return page;
    }

    public int getPerPage() {
        return perPage;
    }

    public ArrayList<WeddingDataModel> getData() {
        return data;
    }

    @Override
    public String toString(){
        return "page: "+page +"\n"+
                "data: "+ data;
    }
}
