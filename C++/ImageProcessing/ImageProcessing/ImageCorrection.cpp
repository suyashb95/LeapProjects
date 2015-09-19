#include "stdafx.h"
#include <iostream>
#include <cstring>
#include "Leap.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <tuple>

using namespace Leap;
using namespace cv;
using namespace std;

class SampleListener : public Listener {
public:
	virtual void onInit(const Controller&);
	virtual void onConnect(const Controller&);
	virtual void onDisconnect(const Controller&);
	virtual void onExit(const Controller&);
	virtual void onFrame(const Controller&);
	virtual void onServiceConnect(const Controller&);
	virtual void onServiceDisconnect(const Controller&);
	virtual Mat slowInterpolation(const Image&);
	virtual tuple<Mat, Mat> getDistortionMaps(const Image&);
	virtual Mat correctImage(const Image&);
	bool distortionInitFlag;
	tuple<Mat, Mat> distortionMaps;
private:

};

const string fingerNames[] = { "Thumb", "Index", "Middle", "Ring", "Pinky" };
const string boneNames[] = { "Metacarpal", "Proximal", "Middle", "Distal" };
const string stateNames[] = { "STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END" };

void SampleListener::onInit(const Controller& controller) {
	distortionInitFlag = false;
	cout << "Initialized" << endl;
}

void SampleListener::onConnect(const Controller& controller) {
	cout << "Connected" << endl;
}

void SampleListener::onDisconnect(const Controller& controller) {
	cout << "Disconnected" << endl;
}

void SampleListener::onExit(const Controller& controller) {
	cout << "Exited" << endl;
}

tuple<Mat, Mat> SampleListener::getDistortionMaps(const Image& image) {

	int destinationHeight = 240;
	int destinationWidth = 640;
	int distortionLength = image.distortionHeight() * image.distortionWidth();
	const float* distortion_buffer = image.distortion();
	float *xmap = new float[distortionLength / 2];
	float *ymap = new float[distortionLength / 2];
	for (int i = 0; i < distortionLength; i += 2) {
		xmap[distortionLength / 2 - i / 2 - 1] = distortion_buffer[i] * destinationWidth;
		ymap[distortionLength / 2 - i / 2 - 1] = distortion_buffer[i + 1] * destinationHeight;
	}
	Mat extended_xmap(image.distortionHeight(), image.distortionWidth() / 2, CV_32FC1, xmap);
	Mat extended_ymap(image.distortionHeight(), image.distortionWidth() / 2, CV_32FC1, ymap);
	resize(extended_xmap, extended_xmap, Size(640, 240), 0, 0, CV_INTER_LINEAR);
	resize(extended_ymap, extended_ymap, Size(640, 240), 0, 0, CV_INTER_LINEAR);
	return make_tuple(extended_xmap, extended_ymap);
}

Mat SampleListener::correctImage(const Image& image) {
	Mat destination(640,240,CV_8UC1,0);
	Mat source(image.height(), image.width(), CV_8UC1, image.dataPointer());
	if (!distortionInitFlag) {
		distortionMaps = getDistortionMaps(image);
		distortionInitFlag = true;
	}
	remap(source,destination,get<0>(distortionMaps),get<1>(distortionMaps), INTER_LINEAR, BORDER_TRANSPARENT);
	return destination;
}

Mat SampleListener::slowInterpolation(const Image& image){
	float destinationWidth = 320;
	float destinationHeight = 120;
	unsigned char destination[320][120];
	float calibrationX, calibrationY;
	float weightX, weightY;
	float dX, dX1, dX2, dX3, dX4;
	float dY, dY1, dY2, dY3, dY4;
	int x1, x2, y1, y2;
	int denormalizedX, denormalizedY;
	int i, j;

	const unsigned char* raw = image.data();
	const float* distortion_buffer = image.distortion();

	const int distortionWidth = image.distortionWidth();
	const int width = image.width();
	const int height = image.height();

	for (i = 0; i < destinationWidth; i++) {
		for (j = 0; j < destinationHeight; j++) {
			calibrationX = 63 * i / destinationWidth;
			calibrationY = 62 * (1 - j / destinationHeight);
			weightX = calibrationX - truncf(calibrationX);
			weightY = calibrationY - truncf(calibrationY);

			x1 = calibrationX;
			y1 = calibrationY;
			x2 = x1 + 1;
			y2 = y1 + 1;
			dX1 = distortion_buffer[x1 * 2 + y1 * distortionWidth];
			dX2 = distortion_buffer[x2 * 2 + y1 * distortionWidth];
			dX3 = distortion_buffer[x1 * 2 + y2 * distortionWidth];
			dX4 = distortion_buffer[x2 * 2 + y2 * distortionWidth];
			dY1 = distortion_buffer[x1 * 2 + y1 * distortionWidth + 1];
			dY2 = distortion_buffer[x2 * 2 + y1 * distortionWidth + 1];
			dY3 = distortion_buffer[x1 * 2 + y2 * distortionWidth + 1];
			dY4 = distortion_buffer[x2 * 2 + y2 * distortionWidth + 1];

			dX = dX1 * (1 - weightX) * (1 - weightY) +
				dX2 * weightX * (1 - weightY) +
				dX3 * (1 - weightX) * weightY +
				dX4 * weightX * weightY;

			dY = dY1 * (1 - weightX) * (1 - weightY) +
				dY2 * weightX * (1 - weightY) +
				dY3 * (1 - weightX) * weightY +
				dY4 * weightX * weightY;

			if ((dX >= 0) && (dX <= 1) && (dY >= 0) && (dY <= 1)) {
				denormalizedX = dX * width;
				denormalizedY = dY * height;

				destination[i][j] = raw[denormalizedX + denormalizedY * width];
			}
			else {
				destination[i][j] = -1;
			}
		}
	}
	Mat undistorted(destinationWidth, destinationHeight,CV_8UC1,destination);
	transpose(undistorted, undistorted);
	return undistorted;
}

void SampleListener::onFrame(const Controller& controller) {
	ImageList images = controller.frame().images();
	if (images[0].isValid() && images[1].isValid()) {
		Mat undistortedLeft = correctImage(images[0]);
		Mat undistortedRight = correctImage(images[1]);
		namedWindow("Left", WINDOW_AUTOSIZE);
		namedWindow("Right", WINDOW_AUTOSIZE);
		imshow("Left", undistortedLeft);
		imshow("Right", undistortedRight);
		waitKey(1);
	}
}

void SampleListener::onServiceConnect(const Controller& controller) {
	cout << "Service Connected" << endl;
}

void SampleListener::onServiceDisconnect(const Controller& controller) {
	cout << "Service Disconnected" << endl;
}

int main(int argc, char** argv) {
	// Create a sample listener and controller
	SampleListener listener;
	Controller controller;

	// Have the sample listener receive events from the controller
	controller.addListener(listener);

	if (argc > 1 && strcmp(argv[1], "--bg") == 0)
	{
		controller.setPolicy(Leap::Controller::POLICY_BACKGROUND_FRAMES);
	}
	controller.setPolicy(Leap::Controller::POLICY_IMAGES);
	// Keep this process running until Enter is pressed
	cout << "Press Enter to quit..." << endl;
	cin.get();
	// Remove the sample listener when done
	controller.removeListener(listener);

	return 0;
}
