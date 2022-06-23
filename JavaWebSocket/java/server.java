import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream; 
import java.io.IOException; 
import java.io.OutputStream; 
import java.net.ServerSocket; 
import java.net.Socket; 
import java.io.InputStream;
import java.io.ObjectInputStream;

public class server { 
    public static int port = 8080;
    public static ServerSocket serverSocket = null; 
    public static String path = "./sample/server/";

    public static void main(String[] args) { 
        try { 
            serverSocket = new ServerSocket(port); 
        } 
        catch (IOException e) { 
            e.printStackTrace(); 
        }
        System.out.println("Wait ... ");

        while(true){
            File dir = new File(path);
            int fileCount = folderFileCount(dir);
            //Socket initSock = null;
    
            // Send file count
            sendFileCount(fileCount);
            
            FileInputStream fileInputStream = null; 
            Socket socket = null; 
    
            int count = 0;
    
            // Send File 
            do{
                try { 
                    socket = serverSocket.accept(); 
                            System.out.println("Inet address: "+socket.getInetAddress());  
        System.out.println("Port number: "+socket.getLocalPort());  
                    OutputStream outputStream = socket.getOutputStream(); 
    
                    String target = path+Integer.toString(count+1)+".png";
    
                    fileInputStream = new FileInputStream(target); 
                    byte[] dataBuff = new byte[10000]; 
                    int length = fileInputStream.read(dataBuff); 
    
                    while (length != -1) { 
                        outputStream.write(dataBuff, 0, length); 
                        length = fileInputStream.read(dataBuff); 
                    } 
                    System.out.println("File \""+ target + "\" is trasmitted!"); 
                } 
                catch (IOException e) { 
                    e.printStackTrace(); 
                } 
        
                finally { 
                    if (fileInputStream != null) { 
                        try { 
                            fileInputStream.close(); 
                        } 
                        catch (IOException e) { 
                            e.printStackTrace(); 
                        } 
                    } 
                    if (socket != null) { 
                        try { 
                            socket.close(); 
                        } 
                        catch (IOException e) { 
                            e.printStackTrace(); 
                        } 
                    } 
                }
                count+=1;
            }while(count<fileCount);
            System.out.println("\n12312312Disconnect\n");

            //getArray();

            System.out.println("\nDisconnect\n");
        }
    } 

    public static int folderFileCount(File givenDir){
        int fileCount = 0;
        try{
            for(File file:givenDir.listFiles()){
                if(file.isFile()){
                    fileCount+=1;
                }
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        return fileCount;
    }

    public static void sendFileCount(int givenFileCount){
        try{
            Socket initSocket = serverSocket.accept();
            OutputStream osInit = initSocket.getOutputStream();
            DataOutputStream dosInit = new DataOutputStream(osInit);
            dosInit.writeInt(givenFileCount);
            System.out.println("File Number '" + givenFileCount+"' is transmitted!\n");
            dosInit.close();
            osInit.close();
            initSocket.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    public static void getArray(){
        try{
            Socket initSocket = serverSocket.accept();
            InputStream osInit = initSocket.getInputStream();
            ObjectInputStream ois = new ObjectInputStream(osInit);
            Object get_object = (Object) ois.readObject();
            System.out.println(get_object);
            ois.close();
            osInit.close();
            initSocket.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
