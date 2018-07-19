#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;
using namespace std;


Rect findMinRect(const Mat1b& src)
{
    Mat1f W(src.rows, src.cols, float(0));
    Mat1f H(src.rows, src.cols, float(0));

    Rect maxRect(0,0,0,0);
    float maxArea = 0.f;

    for (int r = 0; r < src.rows; ++r)
    {
        for (int c = 0; c < src.cols; ++c)
        {
            if (src(r, c) == 0)
            {
                H(r, c) = 1.f + ((r>0) ? H(r-1, c) : 0);
                W(r, c) = 1.f + ((c>0) ? W(r, c-1) : 0);
            }

            float minw = W(r,c);
            for (int h = 0; h < H(r, c); ++h)
            {
                minw = min(minw, W(r-h, c));
                float area = (h+1) * minw;
                if (area > maxArea)
                {
                    maxArea = area;
                    maxRect = Rect(Point(c - minw + 1, r - h), Point(c+1, r+1));
                }
            }
        }
    }

    return maxRect;
}


RotatedRect largestRectInNonConvexPoly(const Mat1b& src, int &finalAngle)
{
    // Create a matrix big enough to not lose points during rotation
    vector<Point> ptz;
    findNonZero(src, ptz);
    Rect bbox = boundingRect(ptz); 
    //cout<< bbox.width<<endl;
    //cout<<bbox.height<<endl;
    int maxdim = max(bbox.width, bbox.height);
    Mat1b work(2*maxdim, 2*maxdim, uchar(0));
    src(bbox).copyTo(work(Rect(maxdim - bbox.width/2, maxdim - bbox.height / 2, bbox.width, bbox.height)));

    // Store best data
    Rect bestRect;
    int bestAngle = 0;

    // For each angle
    for (int angle = 0; angle < 90; angle += 1)
    {
        //cout << angle << endl;

        // Rotate the image
        Mat R = getRotationMatrix2D(Point(maxdim,maxdim), angle, 1);
        Mat1b rotated;
        warpAffine(work, rotated, R, work.size());

        // Keep the crop with the polygon
        vector<Point> pts;
        findNonZero(rotated, pts);
        Rect box = boundingRect(pts);
        //cout<< "box:"<<box.width<< ","<<box.height<<endl; 
	    Mat1b crop = rotated(box).clone();
        
        // Invert colors
        crop = ~crop;
	    double min, max;
	    cv::minMaxLoc(crop, &min, &max); 
        // cout<< "min:"<<min<<"max:"<<max<<endl;
        // Solve the problem: "Find largest rectangle containing only zeros in an binary matrix"
        Rect r = findMinRect(crop);
	    //cout<< "minRect:" << r.width<< ", " << r.height<<endl;
        // If best, save result
        if (r.area() > bestRect.area())
        {
            bestRect = r + box.tl();    // Correct the crop displacement
            bestAngle = angle;
        }
        finalAngle = bestAngle;
    }

    // Apply the inverse rotation
    Mat Rinv = getRotationMatrix2D(Point(maxdim, maxdim), -bestAngle, 1);
    vector<Point> rectPoints{bestRect.tl(), Point(bestRect.x + bestRect.width, bestRect.y), bestRect.br(), Point(bestRect.x, bestRect.y + bestRect.height)};
    vector<Point> rotatedRectPoints;
    transform(rectPoints, rotatedRectPoints, Rinv);

    // Apply the reverse translations
    for (int i = 0; i < rotatedRectPoints.size(); ++i)
    {
        rotatedRectPoints[i] += bbox.tl() - Point(maxdim - bbox.width / 2, maxdim - bbox.height / 2);
    }

    // Get the rotated rect
    RotatedRect rrect = minAreaRect(rotatedRectPoints);

    return rrect;
}



int main(int argc, char** argv)
{
    Mat1b imageMat = imread(argv[1], IMREAD_GRAYSCALE);

    //Binary image
    cv::Mat1b img(imageMat.size(), imageMat.type());

    //Apply thresholding
    cv::threshold(imageMat, img, 100, 255, cv::THRESH_BINARY);
    int angle;
    // Compute largest rect inside polygon
    RotatedRect r = largestRectInNonConvexPoly(img, angle);


    /*cout << "angle is :"<< angle << endl;
    int maxdim = imageMat.rows*imageMat.cols;
    Mat R = getRotationMatrix2D(Point(maxdim,maxdim), angle, 1);
    Mat1b rotated;
    warpAffine(img, rotated, R, img.size());*/

    Point2f points[4];
    r.points(points);


    // Show
    Mat3b res;
    cvtColor(img, res, COLOR_GRAY2BGR);


    for (int i = 0; i < 4; ++i)
    {
        line(res, points[i], points[(i + 1) % 4], Scalar(255, 0, 255), 2);
    }

    Mat mask = cv::Mat(img.size(), CV_8UC1, Scalar(255));     // suppose img is your image Mat
    vector<vector<Point>> pts = { { points[0], points[1], points[2], points[3] } };
    fillPoly(mask, pts, Scalar(0));
    mask = ~ mask;
    imwrite("Result.png", mask);

    return 0;
}
