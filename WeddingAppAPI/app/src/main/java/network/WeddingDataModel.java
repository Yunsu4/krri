package network;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class WeddingDataModel {

    @SerializedName("시군")
    @Expose
    private String serviceID;

    @SerializedName("업체명")
    @Expose
    private String serviceName;

    @SerializedName("도로명주소")
    @Expose
    private String address;

    @SerializedName("전화번호")
    @Expose
    private String phoneNumber;


    public String getServiceID() {
        return serviceID;
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getAddress() {
        return address;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    @Override
    public String toString() {
        return "data{" +
                "시군: " + serviceID + "\n" +
                "업체명: " + serviceName + "\n" +
                "도로명주소: " + address + "\n" +
                "전화번호: " + phoneNumber + "\n" +

                "}";
    }
}
