
/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class Han_Zhang_Max {
    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
        public void map(Object key, Text value, Context context)
        throws IOException, InterruptedException {
            System.out.println("map input: key="+key+", value="+value);

            String line = value.toString();
            String[] values = line.split(",");

            if (!values[1].equals("Summerbrew") && !values[0].equals("bar"))
                context.write(new Text(values[0]), new IntWritable(Integer.parseInt(values[2])));
        }
    }

    public static class IntMaxReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
            System.out.print("reduce input: key="+key+", values=");

            int count = 0;
            int max = 0;
            for (IntWritable val : values) {
                System.out.print(val+ " ");

                count++;
                int price = val.get();
                if(price > max)
                    max = price;
            }
            if(count>1)
                context.write(key, new IntWritable(max));
            System.out.println();
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length < 2) {
            System.err.println("Usage: max <in> [<in>...] <out>");
            System.exit(2);
        }
        Job job = Job.getInstance(conf, "max");
        job.setJarByClass(Han_Zhang_Max.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setReducerClass(IntMaxReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        for (int i = 0; i < otherArgs.length - 1; ++i) {
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[otherArgs.length - 1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
