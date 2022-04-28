package com.example.setup;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import org.deeplearning4j.nn.conf.MultiLayerConfiguration;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.deeplearning4j.nn.conf.Updater;
import org.deeplearning4j.nn.conf.layers.DenseLayer;
import org.deeplearning4j.nn.conf.layers.OutputLayer;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.deeplearning4j.nn.weights.WeightInit;
import org.nd4j.linalg.activations.Activation;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.cpu.nativecpu.NDArray;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.lossfunctions.LossFunctions;
import org.nd4j.nativeblas.Nd4jCpu;

public class MainActivity extends AppCompatActivity {

    final int NUM_SAMPLES = 4;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        INDArray tes = NDArray.

        INDArray test = Nd4j.zeros(1, 4);

    }

    private void startBackgroundThread(){
        Thread thread;
        thread = new Thread(()-> {
            createAndUseNetwork();
        });
        thread.start();
    }
    private void createAndUseNetwork(){

    }

}