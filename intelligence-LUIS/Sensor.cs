using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace LuisBot
{
    [Serializable]
    public class Sensor
    {
        public string Pressure { get; set; }
        public string Temp { get; set; }
        public string Humidity { get; set; }
    }
}