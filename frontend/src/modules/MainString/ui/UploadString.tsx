import { downloadFile } from "@/helpers/downloadFile";
import TextAreaInput from "@/ui/TextAreaInput";
import Typography from "@/ui/Typography";
import { Form, Formik } from "formik";
import { useCallback, useEffect, useState } from "react";
import { fetchFile } from "../api/displayJson";
import { useUploadString } from "../api/useUploadString";
import { IRate, Table } from "./Table";
import test from "./test.json";

export const UploadString = () => {
  const { mutateAsync, isPending, data } = useUploadString();
  const [table, setTable] = useState<IRate[]>();
  const handleSubmit = useCallback(
    (text: string) => {
      if (text.length === 0) return;
      mutateAsync({ data: text });
    },
    [mutateAsync]
  );

  const handleDownloadCsv = useCallback(() => {
    if (data) downloadFile(data.data.result_csv);
  }, [data]);

  const inititalValues = {
    area: "",
  };

  useEffect(() => {
    if (data && !isPending) {
      try {
        fetchFile(data.data.result).then((res: { names: IRate[] }) => {
          console.log(res);
          setTable(res.names);
        });
      } catch (e) {
        setTable(test.names);
      }
    }
  }, [data, isPending]);

  return (
    <Formik onSubmit={() => {}} initialValues={inititalValues}>
      {({ values }) => (
        <Form className="flex flex-col gap-6 w-full">
          <TextAreaInput rows="10" name="area" label="Данные" />
          <button
            className={`my-btn w-full ${
              values.area.length === 0 && "bg-stone-700 hover:bg-stone-700"
            }`}
            onClick={() => handleSubmit(values.area)}
          >
            {isPending ? (
              <span className="loading"></span>
            ) : (
              "Получить стандартизацию"
            )}
          </button>
          {data && !isPending && (
            <>
              <Typography
                variant="h3"
                className="flex gap-2 text-lime-300 mt-10"
              >
                Результат
              </Typography>
              <button className={`my-btn w-52`} onClick={handleDownloadCsv}>
                Скачать таблицу
              </button>
            </>
          )}
          {table && <Table rates={table} />}
        </Form>
      )}
    </Formik>
  );
};
