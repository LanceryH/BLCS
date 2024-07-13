#include <iostream>
#include <Eigen/Dense>

using namespace Eigen;

static RowVectorXd force_applied(double mass_1,RowVectorXd xyz_1, double mass_2, RowVectorXd xyz_2)
{
    double G = 6.67430 * pow(10,-11);
    RowVectorXd distance = xyz_1 - xyz_2;
    RowVectorXd f = G * mass_1 * mass_2 * distance/ pow(distance.norm(),3);
    return f;
}

static RowVectorXd Range_Kutta_4()
{

}

int main()
{
    printf("Hello World!\n");

    RowVectorXd xyz_1(3);
    xyz_1 << 0,100,0;
    RowVectorXd xyz_2(3);
    xyz_2 << 0, 100, 100;

    RowVectorXd result = force_applied(10.0, xyz_1, 10.0, xyz_2);

    std::cout<< result << std::endl;


}


