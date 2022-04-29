package com.example.iris;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.google.flatbuffers.FlatBufferBuilder;

import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.deeplearning4j.nn.conf.layers.DenseLayer;
import org.deeplearning4j.nn.conf.layers.OutputLayer;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.nn.weights.WeightInit;
import org.nd4j.linalg.api.blas.params.MMulTranspose;
import org.nd4j.linalg.api.buffer.DataBuffer;
import org.nd4j.linalg.api.buffer.DataType;
import org.nd4j.linalg.api.shape.LongShapeDescriptor;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.activations.Activation;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.exception.Nd4jNoSuchWorkspaceException;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.indexing.INDArrayIndex;
import org.nd4j.linalg.indexing.conditions.Condition;
import org.nd4j.linalg.string.NDArrayStrings;

import java.nio.LongBuffer;
import java.text.DecimalFormat;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    double first;
    double second;
    double third;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Get references to the editTexts that take the measurements
        final EditText PL = (EditText) findViewById(R.id.editText);
        final EditText PW = (EditText) findViewById(R.id.editText2);
        final EditText SL = (EditText) findViewById(R.id.editText3);
        final EditText SW = (EditText) findViewById(R.id.editText4);

        // Onclick to capture the input and launch the asyncTask
        Button button = (Button) findViewById(R.id.button);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v){
                final double pl = Double.parseDouble(PL.getText().toString());
                final double pw = Double.parseDouble(PW.getText().toString());
                final double sl = Double.parseDouble(SL.getText().toString());
                final double sw = Double.parseDouble(SW.getText().toString());

                AsyncTaskRunner runner = new AsyncTaskRunner();

                // pass the measurement as params to the AsyncTask
                runner.execute(pl, pw, sl, sw);

                ProgressBar bar = (ProgressBar) findViewById(R.id.progressBar);
                bar.setVisibility(View.VISIBLE);
            }
        });
    }

    private class AsyncTaskRunner extends AsyncTask<Double, Integer, String>{

        // Runs in UI before background thread is called
        @Override
        protected void onPreExecute(){
            super.onPreExecute();

            ProgressBar bar = (ProgressBar) findViewById(R.id.progressBar);
            bar.setVisibility(View.INVISIBLE);
        }

        // This is our main Background thread the neural net
        @Override
        protected String doInBackground(Double... params){
            // Get the doubles from params, which is an array so they will be 0, 1, 2, 3
            double pld = params[0];
            double pwd = params[1];
            double sld = params[2];
            double swd = params[3];

            // Create input INDArray for the user measurements
            INDArray actualInput = Nd4j.zeros(1, 4);
            actualInput.putScalar(new int[]{0, 0}, pld);
            actualInput.putScalar(new int[]{0, 1}, pwd);
            actualInput.putScalar(new int[]{0, 2}, sld);
            actualInput.putScalar(new int[]{0, 3}, swd);

            // Convert the iris data into 150x4 matrix
            int row = 150;
            int col = 4;
            double[][] irisMatrix = new double[row][col];
            int i = 0;
            for(int r=0; r<row; r++){
                for(int c=0; c<col; c++){
                    irisMatrix[r][c] = com.example.iris.DataSet.irisData[i++];
                }
            }

            // Now do the same for the label data
            int rowLabel = 150;
            int colLabel = 3;
            double[][] twodimLabel = new double[rowLabel][colLabel];
            int ii=0;
            for(int r=0; r<rowLabel; r++){
                for(int c=0; c<colLabel; c++){
                    twodimLabel[r][c]= com.example.iris.DataSet.labelData[ii++];
                }
            }

            System.out.println(Arrays.deepToString(twodimLabel).replace("], ", "]\n"));

            // Converting the data matrices into training INDArrays is straight forward
            INDArray trainingIn = Nd4j.create(irisMatrix);
            INDArray trainingOut = Nd4j.create(twodimLabel);

            // define the layers of the network
            DenseLayer inputLayer = new DenseLayer.Builder()
                    .nIn(4)
                    .nOut(3)
                    .name("Input")
                    .build();

            DenseLayer hiddenLayer = new DenseLayer.Builder()
                    .nIn(3)
                    .nOut(3)
                    .name("Hidden")
                    .build();

            OutputLayer outputLayer = new OutputLayer.Builder()
                    .nIn(3)
                    .nOut(3)
                    .name("Output")
                    .activation(Activation.SOFTMAX)
                    .build();

            NeuralNetConfiguration.Builder nncBuilder = new NeuralNetConfiguration.Builder();
            long seed = 6;
            nncBuilder.seed(seed);
            nncBuilder.activation(Activation.TANH);
            nncBuilder.weightInit(WeightInit.XAVIER);

            NeuralNetConfiguration.ListBuilder listBuilder = nncBuilder.list();
            listBuilder.layer(0, inputLayer);
            listBuilder.layer(1, hiddenLayer);
            listBuilder.layer(2, outputLayer);

            MultiLayerNetwork myNetwork = new MultiLayerNetwork(listBuilder.build());
            myNetwork.init();

            // Create a data set from the INDArrays and train the network
            DataSet myData = new DataSet(trainingIn, trainingOut);
            for(int e=0; e<=1000; e++){
                myNetwork.fit(myData);
            }

            INDArray actualOutput = myNetwork.output(actualInput);
            Log.d("myNetwork Output ", actualOutput.toString());

            // Retrieve the three Probabilities
            first = actualOutput.getDouble(0,0);
            second = actualOutput.getDouble(0, 1);
            third = actualOutput.getDouble(0, 2);

            // Here we return the INDArray to onPostExecute where it can be
            // used to update the UI
            return actualOutput.toString();
        }

        // This is where we update the UI with our classification results
        @Override
        protected void onPostExecute(String result){
            super.onPostExecute(result);

            // Hide the progress bar now that we are finished
            ProgressBar bar = (ProgressBar) findViewById(R.id.progressBar);
            bar.setVisibility(View.INVISIBLE);


            // Update the UI with output
            TextView setosa = (TextView) findViewById(R.id.textView11);
            TextView versicolor = (TextView) findViewById(R.id.textView12);
            TextView virginica = (TextView) findViewById(R.id.textView13);

            // Limit the double to values to two decimals using DecimalFormat
            DecimalFormat df2 = new DecimalFormat(".##");

            // Set the text of the textViews in UI to show the probabilities
            setosa.setText(String.valueOf(df2.format(first)));
            versicolor.setText(String.valueOf(df2.format(second)));
            virginica.setText(String.valueOf(df2.format(third)));
        }
    }
}

