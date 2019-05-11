// Compile with: $ g++ opencv_gst.cpp -o opencv_gst `pkg-config --cflags --libs opencv`

#include <stdio.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>

int main(int argc, char** argv) {

    // Original gstreamer pipeline: 
    //      == Sender ==
    //      gst-launch-1.0 v4l2src 
    //      ! video/x-raw, framerate=30/1, width=640, height=480, format=RGB 
    //      ! videoconvert
    //      ! x264enc noise-reduction=10000 tune=zerolatency byte-stream=true threads=4
    //      ! mpegtsmux 
    //      ! udpsink host=localhost port=5000
    //      
    //      == Receiver ==
    //      gst-launch-1.0 -ve udpsrc port=5000
    //      ! tsparse ! tsdemux 
    //      ! h264parse ! avdec_h264 
    //      ! videoconvert 
    //      ! ximagesink sync=false

    // first part of sender pipeline
    cv::VideoCapture cap("v4l2src ! video/x-raw, framerate=30/1, width=640, height=480, format=RGB ! videoconvert ! appsink");
    if (!cap.isOpened()) {
        printf("=ERR= can't create video capture\n");
        return -1;
    }

    // second part of sender pipeline
    cv::VideoWriter writer;
    writer.open("appsrc ! videoconvert ! x264enc noise-reduction=10000 tune=zerolatency byte-stream=true threads=4 ! mpegtsmux ! udpsink host=localhost port=9999"
                , 0, (double)30, cv::Size(640, 480), true);
    if (!writer.isOpened()) {
        printf("=ERR= can't create video writer\n");
        return -1;
    }

    cv::Mat frame;
    int key;

    while (true) {

        cap >> frame;
        if (frame.empty())
            break;

        /* Process the frame here */

        writer << frame;
        key = cv::waitKey( 30 );
    }
}