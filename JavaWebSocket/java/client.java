import java.io.DataInputStream;
import java.io.FileOutputStream; 
import java.io.IOException; 
import java.io.InputStream; 
import java.net.Socket;
import java.net.UnknownHostException; 

public class client{ 
    public static String IP = "168.188.128.94";
    public static int port = 8081;
    public static String path = "./sample/client/";
    public static int fileCount = 0;

    public static void main(String[] args) { 
        // Get File Number
        fileCount=getFileCount(IP, port);
        
        int count=0;
        
        //int count=5;

        Socket socket = null; 
        FileOutputStream fileOutputStream = null; 
/*
        // Get Files
        do{
            try { 
                socket = new Socket(IP, port); 
                InputStream inputStream = socket.getInputStream(); 

                String target = path+Integer.toString(count+1)+".jpg";

                fileOutputStream = new FileOutputStream(target); 
                byte[] dataBuff = new byte[10000]; 
                int length = inputStream.read(dataBuff); 

                while (length != -1) { 
                    fileOutputStream.write(dataBuff, 0, length); 
                    length = inputStream.read(dataBuff); 
                } 
                System.out.println("File \"" + target +"\" is saved!");
            } catch (UnknownHostException e) { 
                e.printStackTrace(); 
            } catch (IOException e) { 
                e.printStackTrace(); 
            }            
            
            finally{
                if (fileOutputStream != null) { 
                    try { 
                        fileOutputStream.close(); 
                    } catch (IOException e) { 
                        e.printStackTrace(); 
                    } 
                } 
                if (socket != null) { 
                    try { 
                        socket.close(); 
                    } catch (IOException e) { 
                        e.printStackTrace(); 
                    } 
                }
            }
            count+=1;
        }while(count<fileCount);    
*/
        System.out.println("\nDisconnected!");
    } 

    public static int getFileCount(String givneIP, int givenPort){
        int getFileCount = 0;
        // Receive File Count
        try{
            Socket initSocket = new Socket(IP, port);
            InputStream isInit = initSocket.getInputStream();
            DataInputStream disInit = new DataInputStream(isInit);
            getFileCount = disInit.readInt();
            System.out.println("Received File Count: " + getFileCount +"\n");
            disInit.close();
            isInit.close();
            initSocket.close();
        }catch(Exception e){
            e.printStackTrace();
        }
        return getFileCount;
    }

    
}
