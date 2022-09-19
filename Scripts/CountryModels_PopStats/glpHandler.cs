using System;
using System.IO;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Web;
using System.Net.Http.Headers;
using System.Web.Http;
using Newtonsoft.Json.Linq;
using System.Text;
using System.Configuration;
using CODV2API.DAL;
using System.Linq;
using Newtonsoft.Json;

namespace CODV2API.Handlers.CountryModels_PopStats
{
    /// <summary>
    /// Business for population statistics for the country to manage key schema or functions necessary for visualizations.
    /// Initial generation includes methods to return json for admin levels as any data is available.
    /// Planned are mechanisms to address pagination or formatting, language in the name elements, for instance name_es may include addtional meta info.
    /// Dependency is a config that reference the country iso3, level, language, reference year.
    /// </summary>
    public class glp
    {
        private string _iso3;
        int? _level;
        private string CountryYear = ConfigurationManager.AppSettings["GLPPopStats"];
        private ApplicationContext db = new ApplicationContext();

        public glp(string iso3, int? level)
        {
            this._iso3 = iso3;
            this._level = level;
        }
        //A method to query the entity and return the json and append the CountryYear.
        //ToDo: summarize based on level 
        public object popstats(string iso3, int? level)
        {
            JArray jsonPopstats = new JArray();
            try
            {
                var resquery = db.glp_admpop_adm2.ToList();
                object bdgYear = new { Year = CountryYear };
                var jres = JsonConvert.SerializeObject(resquery);
                JArray resObj = JArray.Parse(jres);
                JObject r = new JObject();
                r["year"] = CountryYear;
                resObj.Add(r);
                //var n = JsonConvert.SerializeObject(resObj);

                jsonPopstats = resObj;//n;
                //System.Web.Http.Results.JsonResult<CODV2API.Models.Country_Models.glp_admpop_adm2> jsonResult;
                //JToken jt = resquery;



            } catch (Exception e)
            {
                throw;
            }

            return jsonPopstats;
        }
        /*
        public static Dictionary<String,int> entityyear(string Path, int? level)
        {
            string node = "";
            string id;
            string cname;
            int svcIdx = 0;
            int adminIdx = 0;
            StringBuilder requestUrlSB = new StringBuilder(Path + "MapServer?f=pjson");
            Dictionary<String, int> highestAdmin = new Dictionary<string, int>();

            HttpWebRequest request = WebRequest.Create(requestUrlSB.ToString()) as HttpWebRequest;
            request.KeepAlive = true;
           
            using (HttpWebResponse response = request.GetResponse() as HttpWebResponse)
            {
                StreamReader responseStream = new StreamReader(response.GetResponseStream());
                var res = responseStream.ReadToEnd();
                JToken jsonObject = JToken.Parse(res);

                foreach (JProperty item in jsonObject)
                {
                    if (item.Name == "layers")
                    {
                        JArray iso2Feat = JArray.Parse(item.Value.ToString());
                        foreach (var jt in iso2Feat)
                        {
                            id = jt["id"].ToString();
                            bool bt = int.TryParse(id, out adminIdx);
                            cname = jt["name"].ToString();

                            if ((cname.Contains("Admin") && (!(cname.Contains("Lines")) && (!(cname.Contains("Points"))))))
                            {
                                highestAdmin.Add(cname, svcIdx);                             
                            }
                            svcIdx = svcIdx + 1;
                        }
                        
                    }
                }
            }

            return highestAdmin;
        }
        */

    }
}
