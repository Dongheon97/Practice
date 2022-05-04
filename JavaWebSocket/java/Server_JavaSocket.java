import java.nio.ByteBuffer;
import javax.imageio.ImageIO;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;

import java.util.ArrayList;
import java.util.List;

public class Server_JavaSocket{
    private static ServerSocket serverSocket;
    private static Socket socket;
    private static int fileCount;
    private static List<String> filenames;

    public static void main(String[] args) throws InterruptedException{
        String dir = "./sample/server/";

        filenames = getFileNames(dir);
        fileCount = filenames.size();

        System.out.println(filenames);
    
        try{
            // Instantiate ServerSocket Class
            serverSocket = new ServerSocket();
            serverSocket.bind(new InetSocketAddress(8080));

            // Connection wait for multiple client
            System.out.println("Connection wait...");
            socket = serverSocket.accept();
            InetSocketAddress isa = (InetSocketAddress) socket.getRemoteSocketAddress();
            System.out.println("Connect Accepted! Client [" + isa.getHostName() + ":" + isa.getPort() + "]\n");

            // Get Data from Client
            InputStream is = socket.getInputStream();

            byte[] byteArr = new byte[512];
            String msg = null;
            int readByteCount = is.read(byteArr);

            if(readByteCount == -1){
                throw new IOException();
            }

            msg = new String(byteArr, 0, readByteCount, "UTF-8");
            System.out.println("Data Received OK!\n");
            System.out.println("Message : " + msg);

            // Send image files to Client
            OutputStream os = socket.getOutputStream();

            msg = Integer.toString(fileCount);
            byteArr = msg.getBytes("UTF-8");
            os.write(byteArr);
            os.flush();
            os.close();
            System.out.println("Data Trasmitted OK!\n");
            
            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            DataOutputStream dos;
            FileInputStream fis;
            File folder;
            int length;
            
            byte[] buffer = new byte[1024];

            dos = new DataOutputStream(socket.getOutputStream());
            // File read
            folder = new File(dir);
            dos.writeInt(folder.listFiles().length); // send file cnt
            System.out.println(folder.listFiles().length);
            for(File file : folder.listFiles()){
                if(file.isFile()){
                    dos.writeUTF(file.getName());
                    fis = new FileInputStream(file);
                    dos.writeLong(file.length());
                    while((length=fis.read(buffer))!=-1){
                        dos.write(buffer, 0, length);
                        dos.flush();
                    }
                }
            }
            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ /

            // int count = 1;
            // while(count <= fileCount){
            //     // Send image files to Client
            //     OutputStream fos = socket.getOutputStream();

            //     // File transmit Start
            //     String pwd = dir + filenames.get(count);
            //     File img = new File(pwd);
            //     if(!img.exists()){
            //         System.out.println("File not Exist");
            //         System.exit(0);
            //     }
                
            //     BufferedImage imgfile = ImageIO.read(img);
            //     ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            //     ImageIO.write(imgfile, "jpg", byteArrayOutputStream);

            //     byte[] size = ByteBuffer.allocate(4).putInt(byteArrayOutputStream.size()).array();
            //     fos.write(size);
            //     fos.write(byteArrayOutputStream.toByteArray());
            //     fos.flush();
            //     System.out.println("Transmit OK!");
                
            //     Thread.sleep(5000);

            //     count += 1;
            //     // File trasmit End
            //     fos.close();
            // }

            os.close();
            is.close();
            socket.close();
        }
        catch(IOException e){
            e.printStackTrace();
            try{ socket.close(); } catch (IOException e1) {e1.printStackTrace();}
        }

        if(!serverSocket.isClosed()){
            try{
                serverSocket.close();
            }
            catch(IOException e){
                e.printStackTrace();
            }
        }
    }

    public static List<String> getFileNames(String givenDir){
        File dir = new File(givenDir);
        String[] names = dir.list();
        
        List<String> list = new ArrayList<String>();
        
        for(String filenames:names){
            if(!filenames.equals(".DS_Store")){
                list.add(filenames);
            }
        }
        return list;
    }

}
