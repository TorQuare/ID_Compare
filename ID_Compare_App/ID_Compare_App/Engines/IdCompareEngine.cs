using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ID_Compare_App.Engines
{
    public class IdCompareEngine : PathClass
    {
        string[] array_to_compare;
        string[] base_array;

        public IdCompareEngine(string[] array_to_compare, string[] base_array)
        {
            this.array_to_compare = array_to_compare;
            this.base_array = base_array;
            start_compare();
        }

        /*
        <Summary>
        Returns and print array with strings which were founded in base array.
        </Summary>
        */
        public string[] compare_duplicates(bool skip)
        {
            string[] found_duplicates = { };
            foreach (string value in array_to_compare)
            {
                foreach (string base_value in base_array)
                {
                    if (value == base_value)
                    {
                        switch (skip)
                        {
                            case true:
                                if (double_check(value, found_duplicates) == false)
                                {
                                    found_duplicates = found_duplicates.Append(value).ToArray();
                                }
                                break;

                            case false:
                                found_duplicates = found_duplicates.Append(value).ToArray();
                                break;
                        }
                    }
                }
            }
            Console.WriteLine(string.Join(" ", found_duplicates));
            return found_duplicates;
        }

        /*
        <Summary>
        Returns and print array with strings which were not founded in base array.
        </Summary>
        */
        public string[] not_found()
        {
            bool found = false;
            string[] not_found = { };
            foreach (string value in array_to_compare)
            {
                foreach (string base_value in base_array)
                {
                    if (value == base_value)
                    {
                        found = true;
                    }
                }
                if (found) { found = false; }
                else { not_found = not_found.Append(value).ToArray(); }
            }
            Console.WriteLine(string.Join(" ", not_found));
            return not_found;
        }


        /*
        <Summary>
        Returns true if given value occurs in founded array.
        </Summary>
        */
        private bool double_check(string value, string[] array_of_found_duplicates)
        {
            foreach (string check_value in array_of_found_duplicates)
            {
                if (value == check_value)
                {
                    return true;
                }
            }
            return false;
        }


        /*
        <Summary>
        An auto engine which execute main methods automatically.
        </Summary>
        */
        private void start_compare()
        {
            bool skip_duplicates = false;
            for (int iterator = 0; iterator <= 1; iterator++)
            {
                if (skip_duplicates)
                {
                    string[] not_found_arr = not_found();
                }
                string[] found_duplicates = compare_duplicates(skip_duplicates);
                skip_duplicates = !skip_duplicates;
            }

        }


    }
}
