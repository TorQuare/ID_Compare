using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ID_Compare_App
{
    /*
    <Summary>
    Class only for collecting names used in other classes and methods.
    </Summary>
    */
    public class PathClass
    {
        // Names of files:
        public string list_to_compare_file_name = "List to compare";
        public string base_list_file_name = "Base list";
        public string not_found_file_name = "Not found";
        public string duplicates_with_skip_file_name = "Duplicates";
        public string duplicates_file_name = "Duplicates full";

        // Extensions:
        public string txt_extension = ".txt";
        public string json_extension = ".json";

        public string[] directories = { "Duplicates", "Not Found" };

        public string path_to_app = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);

    }

    /*
    <Summary>
    Returns name of given file with extension.
    </Summary>
    */
    public class ExtensionBuilder : PathClass
    {
        public string return_txt(string name)
        {
            return name + this.txt_extension;
        }

        public string return_json(string name)
        {
            return name + this.json_extension;
        }
    }
    /*
    <Summary>
    Class used only for break console after program finish his job.
    </Summary>
    */
    public class ConsoleResult
    {
        public ConsoleResult(bool result)
        {
            if (result) 
            {
                Console.WriteLine("Done");
                Console.ReadLine();
            }
            else 
            {
                Console.WriteLine("Need to debug!");
                Console.ReadLine();
            }
        }


    }
}
