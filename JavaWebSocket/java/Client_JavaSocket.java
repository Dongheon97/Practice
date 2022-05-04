import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;

import javax.imageio.ImageIO;

import java.awt.image.BufferedImage;

public class Client_JavaSocket{
    private static Socket socket;
    private static InputStream is;
    private static OutputStream os;
    private static int fileCount;
    private static String dir = "./sample/client/";

    public static void main(String[] args) throws InterruptedException{
        try{
            socket = new Socket();
            System.out.println("Server Connecting..");
            socket.connect(new InetSocketAddress("127.0.0.1", 8080));
            if(!socket.isConnected()){
                System.out.println("Socket Connect Error");
                System.exit(0);
            }
            System.out.println("Server connection OK!\n");

            os = socket.getOutputStream();

            byte[] byteArr = null;
            String msg = "Hello Server";
            
            byteArr = msg.getBytes("UTF-8");
            os.write(byteArr);
            os.flush();
            System.out.println("Data Transmitted OK!\n");

            is = socket.getInputStream();
            byteArr = new byte[512];
            int readByteCount = is.read(byteArr);

            if(readByteCount == -1){
                throw new IOException();
            }
            msg = new String(byteArr, 0, readByteCount, "UTF-8");
            fileCount = Integer.parseInt(msg);
            System.out.println("Data Received OK!\n");
            System.out.println("Message: " + msg);
            System.out.println(fileCount);
            is.close();

            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            DataInputStream dis;
            FileOutputStream fos;
            File file;
            byte[] buffer = new byte[1024];
            int length;

            dis = new DataInputStream(socket.getInputStream());
            int fileCnt = dis.readInt();
            for(int i=0; i<fileCnt; i++){
                String fileName = dis.readUTF();
                file = new File(dir+fileName);
                file.createNewFile();
                System.out.println(file.getName());

                long fileSize = dis.readLong();
                long data = 0;
                fos = new FileOutputStream(file);
                while((length=dis.read(buffer))!=-1){
                    fos.write(buffer, 0, length);
                    data += length;
                    if(data==fileSize){
                        break;
                    }

                }
            }
            // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ /

            int count = 1;
            while(count<=fileCount){
                InputStream fis = socket.getInputStream();
                String pwd = dir + Integer.toString(count) + ".jpg";
                
                // File receive start
                byte[] sizeAr = new byte[4];
                is.read(sizeAr);
                int size = ByteBuffer.wrap(sizeAr).asIntBuffer().get();
                byte[] imageAr = new byte[size];
                is.read(imageAr);
    
                BufferedImage image = ImageIO.read(new ByteArrayInputStream(imageAr));
                ImageIO.write(image, "jpg", new File(pwd));
                System.out.println("Data Received OK!");
                
                Thread.sleep(5000);

                count += 1;
                // File receive end
                fis.close();
            }

            os.close();
        }
        catch(UnknownHostException e){
            e.printStackTrace();
        }
        catch(IOException e){
            e.printStackTrace();
            try{socket.close();} catch(IOException e1){e1.printStackTrace();}
        }

        if(!socket.isClosed()){
            try{
                socket.close();
            }
            catch(IOException e){
                e.printStackTrace();
            }
        }
    }
}

