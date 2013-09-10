#include "smile_linux/smile.h"
#include <iomanip>
#include <iostream>
#include <fstream>
#include <string.h>
#include <sstream>
#include <string>
#include <algorithm>
#include <cmath>
#include <stdio.h>
#include <math.h>

using namespace std;

// g++ -o DCM DCM.cpp -L/usr/local/lib/smile -lsmilearn -lsmile

int main() {
    DSL_network theNet;
    theNet.ReadFile("DCM.xdsl");

    // name of the output files
    const char * output_chloride = "dat/results/t-05-07-a-DCM-dc-0.txt";
    const char * output_failure  = "dat/results/t-05-07-b-DCM-dc-0.txt";

    // use clustering algorithm
    theNet.SetDefaultBNAlgorithm(DSL_ALG_BN_LAURITZEN);

    // introduce the evidence
    // int WCratio = theNet.FindNode("WCratio");
    // int CuringPeriod = theNet.FindNode("CuringPeriod");
    // int Zone = theNet.FindNode("Zone");
    int CoverDepth = theNet.FindNode("CoverDepth");

    // int Temperature = theNet.FindNode("Temperature");
    // int Humidity = theNet.FindNode("Humidity");
    // int Diameter = theNet.FindNode("Diameter");

    // int Chloride_20_0 = theNet.FindNode("HCPM_20_0");

    // 0 is the index of state 1
    // theNet.GetNode(WCratio)->Value()->SetEvidence(0);
    // theNet.GetNode(CuringPeriod)->Value()->SetEvidence(3);
    // theNet.GetNode(Zone)->Value()->SetEvidence(1);
    theNet.GetNode(CoverDepth)->Value()->SetEvidence(0);

    // theNet.GetNode(Temperature)->Value()->SetEvidence(0);
    // theNet.GetNode(Humidity)->Value()->SetEvidence(0);
    // theNet.GetNode(Diameter)->Value()->SetEvidence(0);

    // theNet.GetNode(Chloride_20_0)->Value()->SetEvidence(1);

    // update the network
    theNet.UpdateBeliefs();


    // create output file
    ofstream myfile;
    myfile.open (output_chloride);

    // counter
    double start_age = 0.0;
    double end_age = 50.0;
    double step_age = 1.;

    // loop over all Chloride nodes
    for (double i=start_age; i < end_age+step_age; i+=step_age) {
        // Number to String
        std::ostringstream sstr;
        sstr << i;
        std::string ageAsString = sstr.str();

        // replace "." with "_"
        replace(ageAsString.begin(), ageAsString.end(), '.', '_');

        // node name
        string name = "Chloride_";
        string node,other ="_0";

        double fractpart, intpart;

        fractpart = modf (i , &intpart);
        if (fractpart==0.0)
            {
                node = name+ageAsString+other;
            }
        else
            {
                node = name+ageAsString;
            }

        const char * node_c = node.c_str();

        // get the handle of node "Chloride_i"
        int Chloride = theNet.FindNode(node_c);

        // get the result value
        DSL_sysCoordinates theCoordinates(*theNet.GetNode(Chloride)->Value());
        DSL_idArray *theNames;
        theNames = theNet.GetNode(Chloride)->Definition()->GetOutcomesNames();
        int moderateIndex = theNames->FindPosition("n_corrosion"); // should be 1
        theCoordinates[0] = moderateIndex;
        theCoordinates.GoToCurrentPosition();

        // get probability
        double Chloride_n = theCoordinates.UncheckedValue();

        cout << i <<" : "<< Chloride_n << "\n";

        myfile << i << " " << std::fixed << std::setprecision(16) << Chloride_n << "\n";

    }
    myfile.close();



    // create output file
    // ofstream myfile;
    myfile.open (output_failure);

    // counter
    // double start_age = 0.0;
    // double end_age = 50.0;
    // double step_age = 1.;

    // loop over all Chloride nodes
    for (double i=start_age; i < end_age+step_age; i+=step_age) {
        // Number to String
        std::ostringstream sstr;
        sstr << i;
        std::string ageAsString = sstr.str();

        // replace "." with "_"
        replace(ageAsString.begin(), ageAsString.end(), '.', '_');

        // node name
        // string name = "Chloride_";
        string name = "Failure_";
        string node,other ="_0";

        double fractpart, intpart;

        fractpart = modf (i , &intpart);
        if (fractpart==0.0)
            {
                node = name+ageAsString+other;
            }
        else
            {
                node = name+ageAsString;
            }

        const char * node_c = node.c_str();

        // get the handle of node "Chloride_i"
        int Failure = theNet.FindNode(node_c);

        // get the result value
        DSL_sysCoordinates theCoordinates(*theNet.GetNode(Failure)->Value());
        DSL_idArray *theNames;
        theNames = theNet.GetNode(Failure)->Definition()->GetOutcomesNames();
        int moderateIndex = theNames->FindPosition("n_failure"); // should be 1
        theCoordinates[0] = moderateIndex;
        theCoordinates.GoToCurrentPosition();

        // get probability
        double Failure_n = theCoordinates.UncheckedValue();

        cout << i <<" : "<< Failure_n << "\n";

        myfile << i << " " << std::fixed << std::setprecision(16) << Failure_n << "\n";

    }
    myfile.close();

    return 0;
};
