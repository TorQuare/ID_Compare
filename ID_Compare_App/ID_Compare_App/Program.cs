using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ID_Compare_App
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] array_to_compare = { "VW", "BMW", "123" };
            string[] base_array = { "VW", "Audi", "123", "123" };
            IdCompareEngine base_compare = new IdCompareEngine(array_to_compare, base_array);
        }
    }
}
