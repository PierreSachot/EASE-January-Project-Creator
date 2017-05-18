'''
Creates five projects with java nature
'''
import urllib2
from distutils.sysconfig import project_base

loadModule("/System/Resources")
include('workspace://Utilities/java_array.py')

# https://dzone.com/articles/use-eclipse-jdt-dynamically

IFolder = org.eclipse.core.resources.IFolder
IProject = org.eclipse.core.resources.IProject
IProjectDescription = org.eclipse.core.resources.IProjectDescription
IWorkspaceRoot = org.eclipse.core.resources.IWorkspaceRoot
ResourcesPlugin = org.eclipse.core.resources.ResourcesPlugin
CoreException = org.eclipse.core.runtime.CoreException
IClasspathEntry = org.eclipse.jdt.core.IClasspathEntry
ICompilationUnit = org.eclipse.jdt.core.ICompilationUnit
IJavaProject = org.eclipse.jdt.core.IJavaProject
IPackageFragment = org.eclipse.jdt.core.IPackageFragment
IPackageFragmentRoot = org.eclipse.jdt.core.IPackageFragmentRoot
IType = org.eclipse.jdt.core.IType
JavaCore = org.eclipse.jdt.core.JavaCore
JavaModelException = org.eclipse.jdt.core.JavaModelException
JavaRuntime = org.eclipse.jdt.launching.JavaRuntime

global project


def create_java_project(name):
    global project
    
    project = getProject(name)
    if project.exists():
        raise Exception("Project {} already exists".format(name))
    project = createProject(name)
    description = project.getDescription()
    natureId = org.eclipse.jdt.core.JavaCore.NATURE_ID
    description.setNatureIds(java_array([natureId], java_type=java.lang.String))
    project.setDescription(description, None)

    javaProject = JavaCore.create(project)
    
    download_file("https://github.com/PierreSachot/JanuaryGameOfLife/raw/master/january.jar")

    # set the build path
    buildPath = java_array([JavaCore.newSourceEntry(project.getFullPath().append("src")), JavaRuntime.getDefaultJREContainerEntry(), JavaCore.newLibraryEntry(project.getFullPath().append("january.jar"), None, None)], java_type=IClasspathEntry)
    javaProject.setRawClasspath(buildPath, project.getFullPath().append("bin"), None)

    # create folder by using resources package
    folder = project.getFolder("src")
    folder.create(True, True, None)

    return javaProject

def create_java_package(javaProject, packageName):
    srcFolder = javaProject.getPackageFragmentRoot(javaProject.getProject().getFolder("src"))
    javaPackage = srcFolder.createPackageFragment(packageName, True, None)
    return javaPackage

def create_java_class(javaPackage, className):
    # init code string and create compilation unit
    str = '''package {packageName};

import org.eclipse.january.dataset.DTypeUtils;
import org.eclipse.january.dataset.Dataset;
import org.eclipse.january.dataset.DatasetFactory;
import org.eclipse.january.dataset.DoubleDataset;
import org.eclipse.january.dataset.Random;


public class {className} {{

    public static void main(String[] args)
    {{
        //Creating a 0 initialized Dataset
            //Way 1
            Dataset myZerosDataset = DatasetFactory.createFromObject(new double[] {{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }});
            
            //Way 2
            Dataset myZerosDatasetWay2 = DatasetFactory.zeros(10);
        
            
        // Creating a 1 initialized Dataset
            Dataset myOnesDataset = DatasetFactory.ones(9);
        
            
        //Creating a random values Dataset
            final int[] shape = new int[] {{5}};
            final Dataset myRandomDataset = Random.randn(shape);
        
            
        //Creating Dataset from arrays
            //1D
            final int[] shape1D = new int[] {{5}};
            final Dataset my1DArrayDataset = Random.randn(shape1D);
            
            //2D Way1
            double[][] my2DArrayDatasetValues = {{{{ 1.2, 2.3}}, {{3.4, 4.5}} }};
            Dataset my2DArrayDataset = DatasetFactory.createFromObject(my2DArrayDatasetValues);
            
            //2D Way2
            Dataset my2DArrayDatasetWay2 = DatasetFactory.createFromObject(my2DArrayDatasetValues, 2, 2);
            
            //ND Way1
            double[][][][] myNDDatasetValues = 
                {{{{
                    {{{{ 2, 4}}, {{4, 53}},{{ 12, 14}}, {{14 ,153}}}},
                    {{{{ 3, 5}}, {{5, 54}},{{ 13, 15}}, {{15 ,154}}}}
                }},
                {{
                    {{{{ 4, 6}}, {{6, 55}},{{ 14, 15}}, {{15 ,155}}}},
                    {{{{ 5, 7}}, {{7, 56}},{{ 13, 16}}, {{16 ,156}}}}
                }}}};
            Dataset myNDDataset = DatasetFactory.createFromObject(myNDDatasetValues);
            
            //NDWay2
            double[] myNDDatasetValuesWay2 = {{ 2, 4, 4, 53, 12, 14, 14, 153, 3, 5, 5, 54, 13, 15, 15, 154, 4, 6, 6, 55, 14, 15,
                    15, 155, 5, 7, 7, 56, 13, 16, 16, 156 }};
            Dataset myNDDatasetWay2 = DatasetFactory.createFromObject(myNDDatasetValuesWay2, 2,2,4,2);
            
        
        //Creating Ranges Dataset
            //From 0 to stop-1
            Dataset myRangeDataset = DatasetFactory.createRange(20);

            //From given start to stop-1
            Dataset myRangeDatasetWithStart = DatasetFactory.createRange(2,20, 1, DTypeUtils.getDType(DoubleDataset.class));

            
        //Creating From other Datasets
            Dataset myFirstDataset = Random.randn(new int[]{{6}});
            Dataset myDataset2nd = DatasetFactory.createFromObject(myFirstDataset);
    }}

}}
'''.format(packageName=javaPackage.getElementName(), className=className)

    cu = javaPackage.createCompilationUnit("{className}.java".format(className=className), str,
                    False, None);

def download_file(url):
    global project
    with open(getWorkspace().getLocation().toString() + '/' +project.getFullPath().toString()+'/january.jar','wb') as f:
        f.write(urllib2.urlopen(url).read())
        f.close()
    print "Download Complete!"

javaProject = create_java_project("test")
packageName = "com.kichwacoders.{}".format("test")
javaPackage = create_java_package(javaProject, packageName)
className = "test"[0].upper() + "test"[1:] + "Demo"
create_java_class(javaPackage, className)


