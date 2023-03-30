using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ID_Compare_App.Engines
{
    /*
    <Summary>
    Auto engine for create all directories and files needed to correct app work.
    </Summary>
    */
    public class PrepareEngine : PathClass
    {
        public PrepareEngine() 
        {
            create_directories();
        }

        public void create_directories()
        {
            foreach (string directory_name in this.directories)
            {
                string full_path = this.path_to_app + directory_name;
                PrepareDirectory new_directory = new PrepareDirectory(full_path, directory_name);
            }
        }
    }

    /*
    <Summary>
    Class try to create directories into given path.
    </Summary>
    */
    public class PrepareDirectory
    {
        public PrepareDirectory(string path, string name) 
        {
            try
            {
                if (Directory.Exists(path))
                {
                    Console.WriteLine("Directory exists." + name);
                    return;
                }
                else
                {
                    Directory.CreateDirectory(path);
                    Console.WriteLine("Directory {0} was created at {1}", name, path);
                    return;
                }
            }
            catch (Exception exc)
            {
                Console.WriteLine("Failed: {0}", exc);
                ConsoleResult failed = new ConsoleResult(false);
            }
            finally { }
        }
    }
}
